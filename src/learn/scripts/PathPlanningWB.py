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
        self.VYtoL = 1
        self.VDtoL = 1
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

    # 围捕势力函数
    def WBF(self, x, y, tx, ty):
        dc = ((x-tx)**2 + (y-ty)**2)**0.5  # 目标距离
        KC = 0.9
        KA = 1
        R = 0.85
        L = 1
        DVijx = 0
        DVijy = 0
        DVCx = KC * (dc - R) * (dc ** -1) * (x - tx)
        DVCy = KC * (dc - R) * (dc ** -1) * (y - ty)
        for f in range(1, self.FC):
           dx = x - QJBL.F[str(f)].nowFX
           dy = y - QJBL.F[str(f)].nowFY
           D = (dx ** 2 + dy ** 2) ** 0.5
           DVijx = DVijx + KA * (D - L) * (D ** -1) * (x - tx)
           DVijy = DVijy + KA * (D - L) * (D ** -1) * (y - ty)
        DVx = DVCx + DVijx
        DVy = DVCy + DVijy  # 势能求和
        return DVx, DVy

    # 围捕期望坐标输出
    def WB(self, x, y, DVx, DVy):
        v = 0.3  # 运动速度
        m = DVx / DVy
        vnx = (-DVx / abs(DVx)) * v * abs(m) / ((m ** 2 + 1)**(1/2))
        vny = (-DVy / abs(DVy)) * v * abs(m) / ((m ** 2 + 1)**(1/2))
        print("vnx=%f"%vnx)
        ex = x + vnx
        ey = y + vny
        return ex, ey
