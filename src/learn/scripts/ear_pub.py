#!/usr/bin/env python
# -*- coding: utf-8 -*-

#该文件为算法部分，从串口节点接收数据并进行算法处理
#之后通过expectp发送给其余两个节点
#非定时，在回调函数中进行数据处理

# 该例程将发布/person_info话题，自定义消息类型learning_topic::Person

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



PP = PathPlanning.PathPlanning(5, 1, 0.5, 0.2, 0.5, 3, 0, 0.5, 1, 0)
PPW= PathPlanningWB.PathPlanning(5, 1, 0.5, 0.2, 0.5, 3, 0, 0.5, 1, 0)

expect_info_pub = rospy.Publisher('/expect_info', expectp, queue_size=50)

def ActualInfoCallback(msg):
    rospy.loginfo("Caculater received  actual Info: X:%f  Y:%f ",  msg.x[0], msg.y[0])
    Caculate()
    exp = expectp()
    exp.x[0] =QJBL.S.idealX
    exp.y[0]=QJBL.S.idealY
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
        


def Caculate():
#for (XX) in range (80,120):
    data = np.zeros(13)
    X=8
    Y=8
    # 输入：QJBL.S.idealX,QJBL.S.idealY,QJBL.S.idealD就是AUV当前的X、Y和深度，0，0，0暂时不用管，9，9，1就是目标点的X、Y和深度
    #if data[-1]>0 and data[-1]<6:
        #print(data)
        #print(data[int(data[-1])*2+2])
      #  X = data[int(data[-1])*2+2]
      #  Y = data[int(data[-1])*2+3]

    D=1#随便设的自身位置
    #QJBL.M.M3D[3:5,1:3,]=1
       # D=1
       # np.delete(data,int(data[-1])*2+2)
       # np.delete(data,int(data[-1])*2+2)
    QJBL.F[str(1)].setFLocation(data[4],data[5],1,0,0)
    QJBL.F[str(2)].setFLocation(data[6],data[7],1,0,0)
    QJBL.F[str(3)].setFLocation(data[8],data[9],1,0,0)
    QJBL.F[str(4)].setFLocation(data[10],data[11],1,0,0)
    QJBL.T.setTLocation(9,9,1,0,0)
    print("X,Y=%F %F "% (X,Y))
    #PP.APF(X,Y,D,0, 0, 0, QJBL.T.nowTX,QJBL.T.nowTY , 1)
    # 输出：QJBL.S.idealX,QJBL.S.idealY,QJBL.S.idealD也是期望的AUV当前的X、Y和深度
    [DVX,DVY]=PPW.WBF(X,Y,QJBL.T.nowTX,QJBL.T.nowTY)
    [QJBL.S.idealX,QJBL.S.idealY]=PPW.WB(X,Y,DVX,DVY)
    X += (QJBL.S.idealX-X)*0.3
    Y += (QJBL.S.idealY-Y)*0.3
    

   # print(QJBL.S.idealX,QJBL.S.idealY,QJBL.S.idealD)

for  i in range(100):
        velocity_publisher()

if __name__ == '__main__':
    try:
        velocity_publisher()
    except rospy.ROSInterruptException:
        pass
