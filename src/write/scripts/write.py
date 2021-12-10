#!/usr/bin/env python
# -*- coding: utf-8 -*-

#该文件为算法部分，从串口节点接收数据并进行算法处理
#之后通过expectp发送给其余两个节点
#非定时，在回调函数中进行数据处理

# 该例程将发布/person_info话题，自定义消息类型learning_topic::Person

import numpy as np
import time
import random
import math
##import cv2
##import serial
##import Vision


import rospy
from learn.msg import earphone,vision,expectp

def ActualInfoCallback():
    pass

def velocity_publisher():
	# ROS节点初始化
    rospy.init_node('earphone_pub', anonymous=True)

	# 创建一个Publisher，发布名为/person_info的topic，消息类型为learning_topic::Person，队列长度10
    rate = rospy.Rate(10) 
    #turtle_vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    if  not rospy.is_shutdown():
        
        print ("????????????????")
        rospy.Subscriber("/actual_info", vision, ActualInfoCallback)
        filename = 'programming.txt' 
        with open(filename, 'a') as file_object:

            file_object.write("I also love finding meaning in large datasets.\n")
            file_object.write("I love creating apps that can run in a browser.\n")     
            
              
        rate.sleep()
		# 按照循环频率延时
        








for  i in range(1):
        velocity_publisher()
'''
if __name__ == '__main__':
    try:
        velocity_publisher()
    except rospy.ROSInterruptException:
        pass
'''