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
exp = expectp()

def ActualInfoCallback(msg):
    #rospy.loginfo("Caculater received  actual Info: X:%f  Y:%f ",  msg.x[0], msg.y[0])
    Caculate(msg)
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
        


def Caculate(msg):
#for (XX) in range (80,120):
    for i in  range (3,6):
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
        #QJBL.T.setTLocation(msg.x[0],msg.x[0],1,0,0)
        QJBL.T.setTLocation(9,9,1,0,0)
        
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
