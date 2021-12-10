#!/usr/bin/env python
# -*- coding: utf-8 -*-

#该文件为算法部分，从串口节点接收数据并进行算法处理
#之后通过expectp发送给其余两个节点
#非定时，在回调函数中进行数据处理

# 该例程将发布/person_info话题，自定义消息类型learning_topic::Person

from logging import error
import PathPlanning
import PathPlanningWB
import QJBL
import numpy as np
import time
import random
import math
##import cv2
##import serial
##import Vision


import rospy
from learn.msg import earphone,vision,expectp

EDGEDISTANCE = 6  #模式切换时距离
FORMATDISTANCE = -0.3 #编队前进距离
PP = PathPlanning.PathPlanning(5, 1, 0.5, 0.2, 0.5, 3, 0, 0.5, 1, 0)
PPW= PathPlanningWB.PathPlanning(5, 1, 0.5, 0.2, 0.5, 3, 0, 0.5, 1, 0)


expect_info_pub = rospy.Publisher('/expect_info', expectp, queue_size=50)
exp = expectp()
Fomat=expectp()#机器人的虚拟期望位置

FormatInitFlag=0 #初始化参数
Master = [ 1,1] #虚拟结构质点
SurrondFlag=0 #围捕初始化参数
def ActualInfoCallback(msg):
        #rospy.loginfo("Caculater received  actual Info: X:%f  Y:%f ",  msg.x[0], msg.y[0])
    #Step 1 : 计算距离并判断模式
    Mode = ModeSwitch (msg)  
    global FormatInitFlag
    global SurrondFlag
    if (Mode==1):#目前是编队模式
        if (FormatInitFlag==0):#编队初始化
            FormationInit(msg)
            FormatInitFlag=1
        FormationChange(msg)
    if (Mode==2):#目前是围捕模式
        if(SurrondFlag==0):
            SurrondInit(msg)
            SurrondFlag=1



    Caculate(msg,Mode)


    global exp
    # 发布消息
    expect_info_pub.publish(exp)
    #rospy.loginfo("Publsh person message[%f, %f]", exp.x[0], exp.y[0])    

def velocity_publisher():
	# ROS节点初始化
    rospy.init_node('earphone_pub', anonymous=True)

	# 创建一个Publisher，发布名为/person_info的topic，消息类型为learning_topic::Person，队列长度10

    if not rospy.is_shutdown():
		# 初始化learning_topic::Person类型的消息


        rospy.Subscriber("/actual_info", vision, ActualInfoCallback)

        rospy.spin()
		# 按照循环频率延时
        

def ModeSwitch(act):
    MaxError=0
    for i in range (2,6):
        Errorx = act.x[i]-act.x[0]
        Errory = act.y[i]-act.y[0]
        Error = ( Errory **2)**0.5
        if (Error > MaxError):
            MaxError=Error
    if (MaxError > EDGEDISTANCE):
        return 1
    else:
        return  2

def  FormationInit(act):
    #函数用于找到各机器人的中心作为虚拟结构质点，并计算最大误差作为最大队形
    Center = (act.x[2]+act.x[3]+act.x[4]+act.x[5])/4
    AveError = 0
    for j in range(2,6):
        Errorx = act.x[j]-Center
        AveError+=abs(Errorx)
    AveError=AveError /4
    global Fomat
    Fomat.x[2]=Center-AveError*1.5
    Fomat.x[3]=Center-AveError*0.5
    Fomat.x[4]=Center+AveError*0.5
    Fomat.x[5]=Center+AveError*1.5
    for k in range (2,6):
        Fomat.y[k]=1
def FormationChange(act):
    num=0
    for i in range (2,6):
        if ((act.y[i]-Master[1])>FORMATDISTANCE):
            num +=1
    if (num > 2):#三个机器人都到位了
        Master[1]+=1
        for j in range (2,6):
            Fomat.y[j]=Master[1]

def SurrondInit(act):
    #函数用于找到编队参考点，给定围捕方向
    #Step 1 : 围捕方向
    #Avex = (act.x[2]+act.x[3]+act.x[4]+act.x[5])/4 - act.x[0]
    #Avey = (act.y[2]+act.y[3]+act.y[4]+act.y[5])/4 - act.y[0]
    #if (abs(Avex)>=abs(Avey)):#从X方向过来
    #    if Avex>0:#机器人从X正来
    #        x=1
    #else :#从Y方向过来
    #    x=2 
    global Fomat

    Fomat.x[2]=act.x[0]-1.5
    Fomat.x[3]=act.x[0]-0.5
    Fomat.x[4]=act.x[0]+0.5
    Fomat.x[5]=act.x[0]+1.5

    Fomat.y[2]=act.y[0]
    Fomat.y[3]=act.y[0]-0.7
    Fomat.y[4]=act.y[0]-0.7
    Fomat.y[5]=act.y[0]
        
    


def Caculate(msg,mode):
#for (XX) in range (80,120):
    for i in  range (2,6):
        X = msg.x[i]
        Y = msg.y[i]#循环输入自身位置
        D=1
        #if X==0:X=1
        #if Y == 0: Y=1
        k=1
        for j in range(2,6):
                if j!=i:
                    QJBL.F[str(k)].setFLocation(msg.x[j],msg.y[j],1,0,0)
                    k+=1
                QJBL.F[str(k)].setFLocation(msg.x[0],msg.y[0],1,0,0)
        #QJBL.T.setTLocation(msg.x[0],msg.x[0],1,0,0)
        #if (mode==1):
        QJBL.T.setTLocation(Fomat.x[i],Fomat.y[i],1,0,0)
        #elif (mode==2):
        #    QJBL.T.setTLocation(msg.x[0],msg.y[0],1,0,0)
        #print("robot %d at  %.2f  , %.2f ,which want to go to %.2f , %.2f "%(i,X,Y,Fomat.x[i],Fomat.y[i]))
        PP.APF(X,Y,D,0, 0, 0, QJBL.T.nowTX,QJBL.T.nowTY , 1)
        exp.x[i] = QJBL.S.idealX
        exp.y[i] = QJBL.S.idealY
        #print("Expect ID :%d   X: %.2f  Y : %.2f"  %(i,exp.x[i],exp.y[i]))
        ############
        #目前不确定会不会撞到目标物体上，可能会。但是暂时先不管他，反正有围捕





for  i in range(100):
        velocity_publisher()

if __name__ == '__main__':
    try:
        velocity_publisher()
    except rospy.ROSInterruptException:
        pass
