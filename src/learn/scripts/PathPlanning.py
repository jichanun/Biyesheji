import time
import math
import numpy as np
import random
import time
import math
import QJBL    #全局变量

class PathPlanning():
    def __init__(self, FC, Number, maxSpeedY, maxSpeedD, maxACC, maxDepth, minDepth, safeDIS, timeINT, targetINT):
        # 友方数，AUV编号，最大速度，水平最大加速度，浮潜最大加速度，最大深度，最小深度，安全距离，计算/执行时间间距（受算力制约），期望与目标保持距离
        # 目前无相关数据因此无法考虑最大加速度限制
        # 模型参数
        self.FYtoV = 1     #速度系数
        self.FDtoV = 1.2
        self.VYtoL = 5
        self.VDtoL = 5
        self.MapX = 10     #环境长宽深/m
        self.MapY = 10
        self.MapD = maxDepth - minDepth
        self.GridX = 20   #X轴栅格划分数 
        self.GridY = 20   #Y轴栅格划分数
        self.GridD = 3   #深度栅格划分数

        # AUV参数
        self.FC = FC
        self.Number = Number
        self.maxSpeedY = maxSpeedY
        self.maxSpeedD = maxSpeedD
        self.maxACC = maxACC
        self.maxDepth = maxDepth
        self.minDepth = minDepth
        self.safeDIS = safeDIS
        self.timeINT = timeINT
        self.targetINT = targetINT

        # 人工势场法参数
        self.detectedGridNumber = 2
        self.impactRadius = safeDIS

        # 其他初始化参数
        self.MapXL = self.MapX / self.GridX
        self.MapYL = self.MapY / self.GridY
        self.MapDL = self.MapD / self.GridD

    # 局部路径
    def APF(self, nx, ny, nd, npo, nyo, nv, ntx, nty, ntd):
        #自身，目标的三维坐标，pitch yaw 速度，自己的三维坐标
        d = ((nx - ntx) ** 2 + (ny - nty) ** 2 + (nd - ntd) ** 2) ** 0.5#计算与目标之间的距离
        if d < self.targetINT:#不要撞上
            QJBL.S.idealX = nx
            QJBL.S.idealY = ny
            QJBL.S.idealD = nd
            QJBL.S.idealPO = npo
            QJBL.S.idealYO = nyo
            QJBL.S.idealV = nv
        else:
            FTx,FTy,FTd = self.FT(nx, ny, nd, ntx, nty, ntd)#引力场
            FOx,FOy,FOd = self.FO(nx, ny, nd)#躲避障碍，如果没有就输出0
            FBx,FBy,FBd = self.FB(nx, ny, nd)#躲避碰撞，返回一个值？TODO:上面三个返回的是啥
            Vx = self.FYtoV * (FOx  + FBx)
            Vy = self.FYtoV * (FOy  + FBy)
            Vd = self.FDtoV * (FOd + FTd + FBd)#速度*误差？TODO:是不是误差待考
            VY = (Vx ** 2 + Vy ** 2) ** 0.5#平面移动速度
            if VY > self.maxSpeedY:
                Vx = Vx * (self.maxSpeedY / VY) ** 0.5
                Vy = Vy * (self.maxSpeedY / VY) ** 0.5
            if Vd > self.maxSpeedD:
                Vd = self.maxSpeedD
            Ix = nx + self.timeINT * self.VYtoL * Vx#期望距离=自身位置+时间*速度
            Iy = ny + self.timeINT * self.VYtoL * Vy
            Id = nd + self.timeINT * self.VDtoL * Vd
            cx,cy,cd = self.GridCount(Ix,Iy,Id) # 发入栅格化
            
            if cx == -1 or cy == -1 or cd == -1:#保持机器人在框内  TODO:出框了要让机器人再回来
                Ix,Iy,Id = self.BoundaryConstraint(Ix,Iy,Id)
                cx,cy,cd = self.GridCount(Ix,Iy,Id)
            QJBL.S.idealX = Ix
            QJBL.S.idealY = Iy
            QJBL.S.idealD = Id

    # 栅格环境计算
    def GridCount(self, x, y, d):#输入实际坐标
        if x >= self.MapX or x < 0:
            cx = -1
        else:
            cx = x//self.MapXL#栅格计算法，整数除法，返回当前占总体的比
        if y >= self.MapY or y < 0:
            cy = -1
        else:
            cy = y//self.MapYL
        if d >= self.maxDepth or x < self.minDepth :
            cd = -1
        else:
            cd = d//self.MapDL
        if np.isnan(cx) :##不能出现nan
            cx = -1
        if np.isnan(cy) :
            cy = -1
        if np.isnan(cd) :
            cd = -1
        return int(cx),int(cy),int(cd)

    # 边界约束
    def BoundaryConstraint(self,x,y,d):
        x = max(min(x,self.MapX),0)
        y = max(min(y,self.MapY),0)
        d = max(min(x,self.maxDepth),self.minDepth)
        return x,y,d
    
    # 目标追踪
    def FT(self, x, y, d, tx, ty, td):#输入目标的，和自身的，输出期望的
        #输入目标的，和自身的
        FTx = -(2 * tx - 2 * x) / (4 * ((tx - x) ** 2 + (ty - y) ** 2 + (td - d) ** 2) ** (1 / 2))
        FTy = -(2 * ty - 2 * y) / (4 * ((tx - x) ** 2 + (ty - y) ** 2 + (td - d) ** 2) ** (1 / 2))
        FTd = -(2 * td - 2 * d) / (4 * ((tx - x) ** 2 + (ty - y) ** 2 + (td - d) ** 2) ** (1 / 2))
        return -FTx,-FTy,-FTd
        #输出期望的

    # 障碍躲避
    def FO(self, x, y, d):#输入目标的坐标
        cx,cy,cd = self.GridCount(x,y,d)#输出栅格化占比
        ox = -1
        oy = -1
        od = -1
        Dis = self.MapX                     #环境大小
        gxl = cx - self.detectedGridNumber  #+人工势场法参数，TODO：了解含义
        gxr = cx + self.detectedGridNumber
        gyl = cy - self.detectedGridNumber
        gyr = cy - self.detectedGridNumber
        for gx in range(gxl,gxr+1,1):
            if gx >= 0 and gx < self.GridX:
                for gy in range(gyl,gyr+1,1):
                    if gy >= 0 and gy < self.GridY:
                        for gd in range(0,self.GridD,1):
                            if QJBL.M.M3D[cx,cy,cd] == 1:#改为GXGYGD※
                                dis = ((x - gx * self.MapXL) ** 2 + (y - gy  * self.MapYL) ** 2 + (d - gd * self.MapDL)) ** 0.5
                                if dis < Dis:
                                    Dis = dis
                                    ox = gx * self.MapXL
                                    oy = gy * self.MapYL
                                    od = gd * self.MapDL
        if( Dis < self.impactRadius + self.safeDIS):#如果小于安全距离+与目标保持距离
            FOx = self.FOFunction(x - gx * self.MapXL, Dis)
            FOy = self.FOFunction(y - gy * self.MapYL, Dis)
            FOd = self.FOFunction(d - gd * self.MapDL, Dis)
            print("dis=%f,da=%f"%(Dis,(x - gx * self.MapXL)))
        else:
            FOx = 0
            FOy = 0
            FOd = 0
        print("FOX=%f" %FOx)
        return FOx,FOy,FOd

    # 障碍躲避调节函数
    def FOFunction(self, da, d):
        fo = np.sign(da)*(2*d)/(da+d)*np.tanh(2.645*(self.impactRadius + self.safeDIS)/self.impactRadius-2.645*(d/self.impactRadius))/2 + 0.5
        return fo

    # AUV间避碰
    def FB(self, x, y, d):
        FBx = 0
        FBy = 0
        FBd = 0
        for f in range(1,self.FC):
            dx = x - QJBL.F[str(f)].nowFX
            dy = y - QJBL.F[str(f)].nowFY
            dd = d - QJBL.F[str(f)].nowFD
            D = (dx**2 + dy**2 + dd**2 + 0.0001)**0.5;
            FBx = FBx + self.FBFunction(dx,D)
            FBy = FBy + self.FBFunction(dy,D)
            FBd = FBd + self.FBFunction(dd,D)
        print("FBX=%f" %FBx)
        return FBx,FBy,FBd

    # AUV间避碰调节函数
    def FBFunction(self, da, d):
        fb = math.tanh(2.645-3.9675*(d/self.safeDIS))/2 + 0.5;
        print ("fb=%f" %fb)
        fb = da/d*fb
        return fb


    # 全局路径
    def GeneticAlgorithm(self,PathNumber, spx, spy, gpx, gpy):
        # 起始点x坐标，y坐标，目标点x坐标，y坐标
        # 要求x、y的网格划分数量相同
        # 要求spy<gpy,spx<gpx
        if(self.GridX != self.GridY):
            return -1
        # 性能参数
        Space = QJBL.M.M2D.T
        SpaceLength = self.GridX   
        OrginalGenerationAmount = 30
        MaxGeneLength = 500
        MaxGeneration = 500
        MinIndividualityAmount = 30
        MaxIndividualityAmount = 200
        IdealIndividualityDownLimit = 50
        IdealIndividualityUpLimit = 100
        MaxVariationLength = 10                             # 约为栅格划分数量的1/3
        MinVariationLength = 3                              # 取2—5
        MotherAmount = 5
        MaxEliteIndividualityAmount = PathNumber
        EliteGeneration = 20
        EliteSimilarityRatio = 0.5
        GeneRepelLevel = 99999 * SpaceLength
        HeadGene = spy * SpaceLength + spx
        TailGene = gpy * SpaceLength + gpx
        ChoosedGeneLength = gpy - spy - 1
        NearGeneX = np.array([0,0,-1,1])
        NearGeneY = np.array([1,-1,0,0])
        successflag = 0
        while(1 - successflag):
            PopulationFitness = float('inf')
            Individual = np.zeros((MaxIndividualityAmount,MaxGeneLength),np.int)
            Fitness = np.zeros(MaxIndividualityAmount)
            GeneFitness = QJBL.M.M2D.reshape(-1,1).astype(float)
            GeneFitness[GeneFitness==1] = float('inf')
            EliteIndividuality = np.zeros((MaxEliteIndividualityAmount + 1,MaxGeneLength),np.int)
            EliteImformation = np.zeros((MaxEliteIndividualityAmount + 1,5))  #[适应度 代 基因长度 路径长度 当量路径长度]
            NowEliteFitness = float('inf')
            NowEliteGeneration = 0
            NowElite = 0
            # 初代
            while len([i for i in Individual[:,0] if i != 0]) < OrginalGenerationAmount:
                oa = len(Individual[Individual[:,0]!=0,0])
                Individual[oa,0] = HeadGene
                for gs in range(1,ChoosedGeneLength):
                     gene = random.randint(0,SpaceLength-1)
                     if(oa%2 == 0):
                        while(Space[gene,spy+gs]==1):
                            gene = random.randint(0,SpaceLength-1)
                        NPX = gene
                        NPY = spy + gs
                     else:
                        while(Space[spx+gs,gene]==1):
                            gene = random.randint(0,SpaceLength-1)
                        NPX = spx + gs
                        NPY = gene
                     Individual[oa,gs] = NPY * SpaceLength + NPX
                Individual[oa,gs+1] = TailGene
                # 连续性插值
                ContinuityGeneLength = 1
                GeneLength = ChoosedGeneLength + 2
                while ContinuityGeneLength != GeneLength and GeneLength != MaxGeneLength:
                    cgx = Individual[oa,ContinuityGeneLength-1] % SpaceLength
                    cgy = Individual[oa,ContinuityGeneLength-1] // SpaceLength
                    ucgx = Individual[oa,ContinuityGeneLength] % SpaceLength
                    ucgy = Individual[oa,ContinuityGeneLength] // SpaceLength
                    if max(abs(ucgx-cgx),abs(ucgy-cgy))==1 :
                        if abs(ucgx-cgx)+abs(ucgy-cgy)==2 :
                           if Space[cgx,ucgy] !=1 and Space[ucgx ,cgy] !=1 :
                               ContinuityGeneLength += 1
                           elif Space[cgx,ucgy] !=1 :
                               interpolationgene = ucgy * SpaceLength + cgx
                               Individual[oa,:] = np.concatenate((Individual[oa,0:ContinuityGeneLength],[interpolationgene],Individual[oa,ContinuityGeneLength:MaxGeneLength-1]))
                               GeneLength = len(Individual[oa,Individual[oa,:]!=0])
                               ContinuityGeneLength += 1
                           elif Space[ucgx,cgy] !=1 :
                               interpolationgene = cgy * SpaceLength + ucgx
                               Individual[oa,:] = np.concatenate((Individual[oa,0:ContinuityGeneLength],[interpolationgene],Individual[oa,ContinuityGeneLength:MaxGeneLength-1]))
                               GeneLength = len(Individual[oa,Individual[oa,:]!=0])
                               ContinuityGeneLength += 1
                        else :
                            ContinuityGeneLength += 1
                    else :
                        ngx = (cgx+ucgx)//2
                        ngy = (cgy+ucgy)//2
                        if Space[ngx,ngy]==1 :
                            IfFindGene = 0
                            ChooseNearGeneOrder = random.sample(range(0,4),4)
                            for ng in ChooseNearGeneOrder :
                                interpolationgene = ( ngy + NearGeneY[ng] ) * SpaceLength + ngx + NearGeneX[ng]
                                if Space[ngx + NearGeneX[ng],ngy + NearGeneY[ng]] !=1 and interpolationgene not in Individual[oa,ContinuityGeneLength-1:GeneLength] :
                                    IfFindGene = 1
                                    break
                        else :
                            interpolationgene = ngy * SpaceLength + ngx
                            IfFindGene = 1
                        if IfFindGene == 1:
                            Individual[oa,:] = np.concatenate((Individual[oa,0:ContinuityGeneLength],[interpolationgene],Individual[oa,ContinuityGeneLength:MaxGeneLength-1]))
                            GeneLength = len(Individual[oa,Individual[oa,:]!=0])
                        else :
                            Individual[oa,:] = 0
                            break
            # 进化
            for mg in range(1,MaxGeneration) :
                OldGenerationAmount = len(Individual[Individual[:,0]!=0])
                CompeteCoefficient = (min(max(IdealIndividualityDownLimit,OldGenerationAmount),IdealIndividualityUpLimit) - IdealIndividualityDownLimit ) / ( IdealIndividualityUpLimit - IdealIndividualityDownLimit )
                DieRatio = 0.1 + 0.2 * CompeteCoefficient
                BreedRatio = 0.2 - 0.1 * CompeteCoefficient;
                VariationRatio = 0.3 - 0.3 * CompeteCoefficient;
                CrossoverRatio = 0.1;
                # 适应度
                for i in range(0,MaxIndividualityAmount) :
                    if Individual[i,0] == 0 :
                        Fitness[i] = 0
                    else :
                        if Individual[i,0] != HeadGene or Individual[i,len(Individual[i,Individual[i,:]!=0])-1] != TailGene :
                            Fitness[i] = 0
                            Individual[i,:] = 0
                            continue
                        GeneLength = len(Individual[i,Individual[i,:]!=0])
                        fitness = GeneFitness[Individual[i,0]]
                        for g in range(0,GeneLength-1):
                            lg = Individual[i,g]
                            ng = Individual[i,g+1]
                            if abs(ng-lg) == 1 or abs(ng-lg) == SpaceLength :
                                fitness = fitness + 10 + GeneFitness[ng]
                            else :
                                fitness = fitness + 14 + GeneFitness[ng]
                        Fitness[i] = fitness
                # 精英判定
                nef = min(Fitness[Fitness!=0])
                NowElite = np.where(Fitness==nef)[0][0]
                if NowElite is None :
                    break
                if nef < NowEliteFitness :
                    NowEliteFitness = nef
                    NowEliteGeneration = mg
                else :
                    ec = len(EliteImformation[EliteImformation[:,0]>1,0])
                    if NowEliteGeneration+EliteGeneration < mg and ec!=MaxEliteIndividualityAmount+1 and Individual[NowElite,0]!= 0:
                        negl = len(Individual[NowElite,Individual[NowElite,:]!=0])
                        neig = Individual[NowElite,Individual[NowElite,:]!=0]
                        neig = neig[neig!=HeadGene]
                        neig = neig[neig!=TailGene]
                        ngf = GeneRepelLevel/negl
                        msi = 0
                        msl = 0
                        ifelite = 1
                        # 适应度更新
                        for g in neig :
                            GeneFitness[g] = GeneFitness[g] + ngf
                        # 相似度
                        for i in range(0,ec) :
                            Intersect = [i for i in EliteIndividuality[i,:] if i in Individual[NowElite,:]]
                            Intersect = np.array(Intersect)
                            Intersect = Intersect[Intersect!=0]
                            fsimilarity = len(Intersect)/negl
                            ssimilarity = len(Intersect)/EliteImformation[i,2]
                            if min(fsimilarity,ssimilarity) > EliteSimilarityRatio :
                                if  msl < ssimilarity :
                                    msl = ssimilarity
                                    msi = i
                                ifelite = 0
                        for i in range(0,ec+1) :
                            EliteIndividuality[ec,:] = Individual[NowElite,:]
                            EliteImformation[ec,1] = NowEliteGeneration
                            EliteImformation[ec,2] = negl
                            GeneLength = len(EliteIndividuality[i,EliteIndividuality[i,:]!=0])
                            fitness = GeneFitness[EliteIndividuality[i,0]]
                            purefitness = 0
                            for g in range(0,GeneLength-1) :
                                lg = EliteIndividuality[i,g]
                                ng = EliteIndividuality[i,g+1]
                                if abs(ng-lg)==1 or abs(ng-lg)==SpaceLength :
                                    purefitness = purefitness + 10
                                    fitness = fitness + 10 + GeneFitness[ng]
                                else :
                                    purefitness = purefitness + 14
                                    fitness = fitness + 14 + GeneFitness[ng]
                                EliteImformation[i,[0,3,4]] = [fitness,purefitness,purefitness]
                        if ifelite==1 :
                            if ec==MaxEliteIndividualityAmount :
                                EliteImformation[ec,:] = 0
                                EliteIndividuality[ec,:] = 0
                        else :
                            legl = EliteImformation[msi,2]
                            leig = EliteIndividuality[msi,EliteIndividuality[msi,:]!=0]
                            leig = leig[leig!=HeadGene]
                            leig = leig[leig!=TailGene]
                            lgf = GeneRepelLevel/legl
                            if EliteImformation[msi,0]>EliteImformation[ec,0] :
                                for g in leig :
                                    GeneFitness[g] = GeneFitness[g] - lgf
                                EliteIndividuality[msi,:] = EliteIndividuality[ec,:]
                                EliteImformation[msi,:] = EliteImformation[ec,:]
                            else :
                                for g in neig:
                                    GeneFitness[g] = GeneFitness[g] - ngf
                            EliteIndividuality[ec,:] = 0
                            EliteImformation[ec,:] = 0
                        NowEliteFitness = float('inf')
                        crossoverelitegene = 0
                        for e1 in range(0,ec) :
                            for e2 in range(e1+1,ec) :
                                Intersect = [i for i in EliteIndividuality[e1,:] if i in EliteIndividuality[e2,:]]
                                Intersect = np.array(Intersect)
                                Intersect = Intersect[Intersect!=0]
                                if len(Intersect) > 2:
                                    crossoverelitegene = Intersect[2]
                                    break
                            if crossoverelitegene!=0 :
                                break
                        if crossoverelitegene!=0 :
                            mothergenebreakpoint = np.where(EliteIndividuality[e1,:]==crossoverelitegene)[0][0]
                            fathergenebreakpoint = np.where(EliteIndividuality[e2,:]==crossoverelitegene)[0][0]
                            son = np.concatenate((EliteIndividuality[e1,0:mothergenebreakpoint],[crossoverelitegene],EliteIndividuality[e2,fathergenebreakpoint+1:MaxGeneLength]))
                            daughter = np.concatenate((EliteIndividuality[e2,0:fathergenebreakpoint],[crossoverelitegene],EliteIndividuality[e1,mothergenebreakpoint+1:MaxGeneLength]))
                            son = son[son!=0]
                            daughter = daughter[daughter!=0]
                            EliteIndividuality[e1,:] = np.concatenate((son,np.zeros(MaxGeneLength-len(son),np.int)))
                            EliteIndividuality[e2,:] = np.concatenate((daughter,np.zeros(MaxGeneLength-len(daughter),np.int)))
                            EmptyIndividualID = 0
                            while EmptyIndividualID != MaxIndividualityAmount and Individual[EmptyIndividualID,0] != 0 :
                                EmptyIndividualID = EmptyIndividualID + 1
                            Individual[EmptyIndividualID,:] = EliteIndividuality[e1,:]
                            Fitness[EmptyIndividualID] = EliteImformation[e1,0]
                            while EmptyIndividualID != MaxIndividualityAmount and Individual[EmptyIndividualID,0] != 0 :
                                EmptyIndividualID = EmptyIndividualID + 1
                            Individual[EmptyIndividualID,:] = EliteIndividuality[e2,:]
                            Fitness[EmptyIndividualID] = EliteImformation[e2,0]
                        #print(mg,EliteImformation)

                # 淘汰选择
                OldGeneration = np.where(Individual[:,0]!=0)[0]
                OldGenerationAmount = len(OldGeneration)
                if OldGenerationAmount > MinIndividualityAmount :
                    for i in OldGeneration:
                        if DieRatio > random.random() :
                            MidGeneration = np.where(Individual[:,0]!=0)[0].T
                            MidGenerationAmount = len(Individual[Individual[:,0]!=0,0])
                            candidatedeath = [ i,MidGeneration[random.sample(range(0,MidGenerationAmount),1)[0]]]  #######################
                            death = np.where(candidatedeath==np.max(candidatedeath))[0][0]
                            Individual[candidatedeath[death],:] = 0
                            Fitness[candidatedeath[death]] = 0
                # 个体繁殖
                EmptyIndividualID = 0
                OldGeneration = np.array(np.where(Individual[:,0]!=0)[0])
                for i in OldGeneration :
                    if BreedRatio > random.random() :
                        while EmptyIndividualID != MaxIndividualityAmount and Individual[EmptyIndividualID,0] != 0 :
                            EmptyIndividualID += 1
                        Individual[EmptyIndividualID,:] = Individual[i,:]
                        Fitness[EmptyIndividualID] = Fitness[i]
                # 复制变异
                EmptyIndividualID = 0
                OldGeneration = np.where(Individual[:,0]!=0)[0]
                for i in OldGeneration :
                    VariationLength = MaxVariationLength -  mg // ( MaxGeneration + 1) * ( MaxVariationLength - MinVariationLength + 1)
                    if VariationRatio > random.random() :
                        while EmptyIndividualID != MaxIndividualityAmount and Individual[EmptyIndividualID,0] != 0 :
                            EmptyIndividualID += 1
                        GeneLength = len(Individual[i,Individual[i,:]!=0])
                        #print('339before',Individual[i,0:30],Fitness[i],GeneLength)
                        worsegenefitness = max(GeneFitness[Individual[i,Individual[i,:]!=0]])[0]
                        worsegene = np.where(GeneFitness==worsegenefitness)[0]
                        worsegene = [k for k in Individual[i,Individual[i,:]!=0] if k in worsegene ]
                        worsegene = np.where(Individual[i,:]==worsegene)[0]
                        IsWorsegene = 0
                        if len(worsegene):
                            worsegene = worsegene[0]
                            IsWorsegene = 1
                        IfSingleWorseGene = 0
                        if worsegenefitness > 1 and IsWorsegene:
                            worsegeneamount = np.array([ i[0] for i in GeneFitness[Individual[i,Individual[i,:]!=0]]])
                            worsegeneamount = len(worsegeneamount[worsegeneamount>1])
                            if worsegeneamount==1 :
                                vs = worsegene-1
                                ve = worsegene+1
                                VariationLength = ve - vs
                                IfSingleWorseGene = 1
                            else :
                                vl = random.sample(range(1,VariationLength),2)
                                vl.sort()
                                vs = max(0,worsegene-vl[0])
                                ve = min(GeneLength,worsegene+vl[1]-vl[0])
                                VariationLength = ve - vs
                        else :
                            vs =  random.sample(range(0,GeneLength - VariationLength),1)[0]
                            VariationLength = random.sample(range(1,VariationLength),1)[0]
                            ve = vs + VariationLength
                        Individual[EmptyIndividualID,:] = np.concatenate((Individual[i,0:vs+1],Individual[i,ve:MaxGeneLength+1],np.zeros((VariationLength-1),np.int)))
                        cgx = Individual[EmptyIndividualID,vs]%SpaceLength
                        cgy = Individual[EmptyIndividualID,vs]//SpaceLength
                        ucgx = Individual[EmptyIndividualID,vs+1]%SpaceLength
                        ucgy = Individual[EmptyIndividualID,vs+1]//SpaceLength
                        if IfSingleWorseGene==0 :
                            if abs(ucgx-cgx)+abs(ucgy-cgy)==1 :
                                GeneInput = 0
                            else :
                                vss = 0
                                VariationSpaceX = np.zeros((abs(ucgx-cgx)+1)*(abs(ucgy-cgy)+1),np.int)
                                VariationSpaceY = np.zeros((abs(ucgx-cgx)+1)*(abs(ucgy-cgy)+1),np.int)
                                for j in range(min(cgx,ucgx),max(cgx,ucgx)) :
                                    for k in range(min(cgy,ucgy),max(cgy,ucgy)) :
                                        if Space[j,k] != 1 :
                                            vss = vss + 1
                                            VariationSpaceX[vss] = j
                                            VariationSpaceY[vss] = k
                                if vss != 0:
                                    vss = random.sample(range(0,vss),1)[0]
                                if vss != 0 and vss != len(VariationSpaceX[:]!=0) :
                                    interpolationgene = VariationSpaceY[vss] * SpaceLength + VariationSpaceX[vss]
                                    if interpolationgene not in Individual[EmptyIndividualID,:] :
                                        Individual[EmptyIndividualID,:] = np.concatenate((Individual[i,0:vs+1],[interpolationgene],Individual[EmptyIndividualID,vs+1:MaxGeneLength-1]))
                                        GeneInput = 1
                                    else :
                                        GeneInput = 0
                                else :
                                    GeneInput = 0
                        else :
                            GeneInput = 0
                            ChooseNearGeneOrder = random.sample(range(0,4),4)
                            ngx = Individual[i,worsegene]%SpaceLength
                            ngy = Individual[i,worsegene]//SpaceLength
                            for ng in ChooseNearGeneOrder :
                                interpolationgene = ( ngy + NearGeneY[ng] ) * SpaceLength + ngx + NearGeneX[ng]
                                if interpolationgene > 0 and ngx + NearGeneX[ng] < SpaceLength and ngy + NearGeneY[ng] < SpaceLength :
                                    if Space[ngx + NearGeneX[ng],ngy + NearGeneY[ng]] !=1 and interpolationgene not in Individual[EmptyIndividualID,vs:ve+1] and GeneFitness[interpolationgene]==0 :
                                        Individual[EmptyIndividualID,:] = np.concatenate((Individual[EmptyIndividualID,0:vs+1],[interpolationgene],Individual[EmptyIndividualID,vs+1:MaxGeneLength-1]))
                                        GeneInput = 1
                                        break
                        GeneLength = GeneLength - VariationLength - 1 + GeneInput
                        ve = vs + 1 + GeneInput
                        while vs != ve and GeneLength != MaxGeneLength :
                            cgx = Individual[EmptyIndividualID,vs]%SpaceLength
                            cgy = Individual[EmptyIndividualID,vs]//SpaceLength
                            ucgx = Individual[EmptyIndividualID,vs+1]%SpaceLength
                            ucgy = Individual[EmptyIndividualID,vs+1]//SpaceLength
                            if cgx==ucgx and cgy==ucgy :
                                Individual[EmptyIndividualID,:] = np.concatenate((Individual[i,0:vs+1],Individual[i,vs+2:MaxGeneLength],[0]))
                                vs = vs + 1
                                break
                            elif max(abs(ucgx-cgx),abs(ucgy-cgy))==1 :
                                if abs(ucgx-cgx)+abs(ucgy-cgy)==2 :
                                    if Space[cgx,ucgy] !=1 and Space[ucgx ,cgy] !=1 :
                                        vs = vs + 1
                                    elif Space[cgx,ucgy] !=1 :
                                        interpolationgene = ucgy * SpaceLength + cgx
                                        Individual[EmptyIndividualID,:] = np.concatenate((Individual[EmptyIndividualID,0:vs+1],[interpolationgene],Individual[EmptyIndividualID,vs+1:MaxGeneLength-1]))
                                        GeneLength = GeneLength + 1
                                        ve = ve + 1
                                        vs = vs + 1
                                    elif Space[ucgx,cgy] !=1 :
                                        interpolationgene = cgy * SpaceLength + ucgx
                                        Individual[EmptyIndividualID,:] = np.concatenate((Individual[EmptyIndividualID,0:vs+1],[interpolationgene],Individual[EmptyIndividualID,vs+1:MaxGeneLength-1]))
                                        GeneLength = GeneLength + 1
                                        ve = ve + 1
                                        vs = vs + 1
                                else :
                                    vs = vs + 1
                            else :
                                ngx = (cgx+ucgx+math.floor(2*random.random()))//2
                                ngy = (cgy+ucgy+math.floor(2*random.random()))//2
                                if Space[ngx,ngy]==1 :
                                    IfFindGene = 0
                                    ChooseNearGeneOrder = random.sample(range(0,4),4)
                                    for ng in ChooseNearGeneOrder :
                                        interpolationgene = ( ngy + NearGeneY[ng] ) * SpaceLength + ngx + NearGeneX[ng]
                                        if Space[ngx + NearGeneX[ng],ngy + NearGeneY[ng]] !=1 and interpolationgene not in Individual[EmptyIndividualID,vs:ve+1] :
                                            IfFindGene = 1
                                            break
                                else :
                                    interpolationgene = ngy * SpaceLength + ngx
                                    IfFindGene = 1
                                if IfFindGene == 1 :
                                    if GeneLength==MaxGeneLength :
                                        Individual[EmptyIndividualID,:] = 0
                                        geneinput = MaxGeneLength
                                        break
                                    Individual[EmptyIndividualID,:] = np.concatenate((Individual[EmptyIndividualID,0:vs+1],[interpolationgene],Individual[EmptyIndividualID,vs+1:MaxGeneLength-1]))
                                    GeneLength = GeneLength + 1
                                    ve = ve + 1
                                else :
                                    Individual[EmptyIndividualID,:] = 0
                                    geneinput = MaxGeneLength
                                    break
                        if Individual[EmptyIndividualID,0] != 0 :
                            # 杀死变异本体
                            #               Individual[i,:] = 0
                            #               Fitness[i] = 0
                            GeneLength = len(Individual[EmptyIndividualID,Individual[EmptyIndividualID,:]!=0])
                            fitness = 0
                            for g in range(0,GeneLength-1) :
                                lg = Individual[EmptyIndividualID,g]
                                ng = Individual[EmptyIndividualID,g+1]
                                if abs(ng-lg)==1 or abs(ng-lg)==SpaceLength :
                                    fitness = fitness + 10
                                else :
                                    fitness = fitness + 14
                            Fitness[EmptyIndividualID] = fitness
                # 交叉变异
                OldGeneration = np.where(Individual[:,0]!=0)[0]
                OldGenerationAmount = len(Individual[Individual[:,0]!=0,0])
                for father in OldGeneration :
                    if CrossoverRatio > random.random() :
                        fathergene = Individual[father,:]
                        fathergene = fathergene[fathergene!=0]
                        qualifiedmother = np.zeros((MotherAmount,2),np.int)
                        candidatemother = OldGeneration[random.sample(range(0,OldGenerationAmount),OldGenerationAmount)]
                        candidatemother = candidatemother[candidatemother!=father]
                        motheramount = 0
                        for cm in candidatemother :
                            ifmother = np.array([ i for i in Individual[cm,:] if i in fathergene])
                            ifmother = ifmother[ifmother!=HeadGene]
                            ifmother = ifmother[ifmother!=TailGene]
                            if len(ifmother):
                                qualifiedmother[motheramount,0] = cm
                                qualifiedmother[motheramount,1] = ifmother[random.sample(range(0,len(ifmother)),1)]
                                motheramount += 1
                            if motheramount==MotherAmount :
                                break
                        qualifiedmother = qualifiedmother[qualifiedmother[:,0]!=0,:]
                        if motheramount!=0 :                                                                                               # ?
                            mother = np.where( i for i in range(0,motheramount) if abs(Fitness[father] - Fitness[qualifiedmother[i,0]]) == max(abs(Fitness[father] - Fitness[qualifiedmother[:,0]])))[0][0]
                            crossovergene = qualifiedmother[mother,1]
                            mother = qualifiedmother[mother,0]
                        else :
                            continue
                        mothergenebreakpoint = np.where(Individual[mother,:]==crossovergene)[0][0]
                        fathergenebreakpoint = np.where(Individual[father,:]==crossovergene)[0][0]
                        son = np.concatenate((Individual[mother,0:mothergenebreakpoint],[crossovergene],Individual[father,fathergenebreakpoint+1:MaxGeneLength]))
                        daughter = np.concatenate((Individual[father,0:fathergenebreakpoint],[crossovergene],Individual[mother,mothergenebreakpoint+1:MaxGeneLength]))
                        son = son[son!=0]
                        daughter = daughter[daughter!=0]
                        if max(len(son),len(daughter)) <= MaxGeneLength :
                            Individual[father,:] = np.concatenate((son,np.zeros(MaxGeneLength-len(son),np.int)))
                            Individual[mother,:] = np.concatenate((daughter,np.zeros(MaxGeneLength-len(daughter),np.int)))
                            for i in [father,mother] :
                                GeneLength = len(Individual[i,Individual[i,:]!=0])
                                fitness = 0
                                for g in range(0,GeneLength-1) :
                                    lg = Individual[i,g]
                                    ng = Individual[i,g+1]
                                    if abs(ng-lg)==1 or abs(ng-lg)==SpaceLength :
                                        fitness = fitness + 10
                                    else :
                                        fitness = fitness + 14
                                Fitness[i] = fitness

            # 进化结果验证
            pathContactLength = 0
            #EVOResult = Space.T
            #for i in range(0,1):
            #    GL = len(EliteIndividuality[i,EliteIndividuality[i,:]!=0])
            #    for G in range(0,GL):
            #        g = EliteIndividuality[i,G]
            #        x = g%SpaceLength
            #        y = g//SpaceLength
            #        if Space[x,y] == 0 :
            #            EVOResult[y,x] = 7
            #        else:
            #            EVOResult[y,x] = 9
            #for i in range(SpaceLength-1,-1,-1):
            #    print(EVOResult[i,:])
            #路径点序列/未测试
            for p in range(0,MaxEliteIndividualityAmount):
                PathLength = len(EliteIndividuality[p,EliteIndividuality[p,:]!=0])
                self.names = globals()
                self.names['PathX%s' % p] = EliteIndividuality[p,0:PathLength]//20 + 1
                self.names = globals()
                self.names['PathY%s' % p] = EliteIndividuality[p,0:PathLength]%20 + 1
                #print(EliteIndividuality[p,0:PathLength])
                #print('PX',p,self.names['PathX%s' % p])
                #print('PY',p,self.names['PathY%s' % p])
            #
            for i in range(0,MaxEliteIndividualityAmount):
                for k in range(0,i):
                    if k < i :
                        ContactGene = [ j for j in EliteIndividuality[k,:] if j in EliteIndividuality[i,:] ]
                        ContactGene = np.array(ContactGene)
                        ContactGene = ContactGene[ContactGene!=0]
                        #print(ContactGene)
                        #print(i,k,len(ContactGene)-2)
                        pathContactLength = pathContactLength + len(ContactGene) - 2
            print(pathContactLength)
            if len(EliteImformation[EliteImformation[:,0]!=0,0]) == MaxEliteIndividualityAmount and pathContactLength==0 :
                successflag = 1
                print('successful')
    
