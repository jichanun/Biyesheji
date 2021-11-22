import numpy as np

class Friend():  #友方信息
    def __init__(self,number,x,y,d,po,yo):
        self.Number=number
        self.nowFX=x             #X坐标
        self.nowFY=y             #Y坐标
        self.nowFD=d             #深度
        self.nowFPO=po           #俯仰角
        self.nowFYO=yo           #偏航角
        self.nowFV=0             #速度
        
    def setFLocation(self,x,y,d,po,yo):
        self.nowFX=x             #X坐标
        self.nowFY=y             #Y坐标
        self.nowFD=d             #深度
        self.nowFPO=po           #俯仰角
        self.nowFYO=yo           #偏航角

class Target():
    def __init__(self,number,x,y,d,po,yo):  #敌方信息
        self.Number=number
        self.nowTX=x            #X坐标
        self.nowTY=y            #Y坐标
        self.nowTD=d            #深度
        self.nowTPO=po          #俯仰角
        self.nowTYO=yo          #偏航角
        self.nowTV=0            #速度
    
    def setTLocation(self, x, y, d, po, yo):
        self.nowTX=x            #X坐标
        self.nowTY=y            #Y坐标
        self.nowTD=d            #深度
        self.nowTPO=po          #俯仰角
        self.nowTYO=yo          #偏航角

class Self():
    def __init__(self,number,x,y,d,po,yo):
        self.Number = number
        self.nowX=x             #X坐标
        self.nowY=y             #Y坐标
        self.nowD=d             #深度
        self.nowPO=po           #俯仰角
        self.nowYO=yo           #偏航角
        self.nowV=0             #速度
        self.idealX=x
        self.idealY=y
        self.idealD=d
        self.idealPO=po
        self.idealYO=yo
        self.idealV=0
        
    def setSLocation(self,x,y,d,po,yo):
        self.nowX=x             #X坐标
        self.nowY=y             #Y坐标
        self.nowD=d             #深度
        self.nowPO=po           #俯仰角
        self.nowYO=yo           #偏航角

class Map():
    def __init__(self,gridX,gridY,gridD):
        if gridD==0 :
            self.M2D = np.zeros((gridX,gridY),np.int)
        else:
            self.M2D = np.zeros((gridX,gridY),np.int)
            self.M3D = np.zeros((gridX,gridY,gridD),np.int)  

if __name__ != "__main__":    # 如果不是主函数就定义一个全局变量
    FC = 5
    TC = 1
    gridX = 20
    gridY = 20
    Number = 1
    count = 1
    F = locals()
    for f in range(1,FC):
        if f == Number:
            count += 1
        F[str(f)] = Friend(count,0,0,1,0,0)
        
        
    T = Target(1,0,0,1,0,0)

            #names = globals()
            #names['T%s' % t] = Target(t,0,0,0,0,0)
    S = Self(Number,0,0,1,0,0)
    M = Map(gridX,gridY,3)

# test map
    M.M2D[3:8,3:5]= 1
    M.M2D[6:11,13:15] = 1
    M.M2D[14:16,6:12]= 1
    M.M2D[8:10,8:11]= 1
    M.M2D[15:17,15:17]= 1
    M.M2D[16:18,2:4]= 1
    M.M2D[3,9]= 1
    M.M2D[11,17]= 1
    M.M2D[2,16]= 1
    M.M2D[11,1]= 1
    M.M2D[10:12,6]= 1
    M.M2D[13:17,13]= 1
    M.M2D[5,6:9]= 1