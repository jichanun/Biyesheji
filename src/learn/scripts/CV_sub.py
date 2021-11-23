#!/usr/bin/env python
# -*- coding: utf-8 -*-

#该部分从串口节点读取实际位置，从算法节点读取期望位置，并绘制图像



from rosgraph.names import anonymous_name
import rospy

from learn.msg import vision,expectp
import math
import numpy as np
import time
import serial #导入serial包

def node():
    #rospy.init_node("serial_test") #初始化ros节点
    ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1) #打开串口, 端口号:"/dev/ttyUSB0". 波特率:9600. 延时等待1s
    print("serial:::::::::::")
    if ser.isOpen(): #判断串口是否打开
        print("串口打开成功")
    else:
        print("串口打开失败")
        quit()
    while not rospy.is_shutdown():
        ser.write('h'.encode())#发送hello
        cnt = ser.inWaiting() #等待接受数据
        if cnt > 0 : #接受数据量大于0
            rev = ser.read(cnt) #读数据
            print(len(rev)) #打印
            break



def ActualInfoCallback(msg):
    #rospy.loginfo("CV received Actual position: X:%f  Y:%f ", msg.x[0], msg.y[0])
    pass
def ExpectInfoCallback(msg):
    #rospy.loginfo("CV received Expected position x:%f y:%f", msg.x[0],msg.y[0])
    pass
def person_subscriber():
	# ROS节点初始化
    rospy.init_node('CV_sub', anonymous=True)

	# 创建一个Subscriber，订阅名为/person_info的topic，注册回调函数personInfoCallback
    rospy.Subscriber("/actual_info", vision, ActualInfoCallback)
    rospy.Subscriber("/expect_info", expectp, ExpectInfoCallback)

	# 循环等待回调函数
    rospy.spin()

if __name__ == '__main__':
    person_subscriber()
