#!/usr/bin/env python
# -*- coding: utf-8 -*-

#该部分从串口节点读取实际位置，从算法节点读取期望位置，并绘制图像



from rosgraph.names import anonymous_name
import rospy

from learn.msg import vision,expectp
import cv2
import numpy as np 
import time
import matplotlib.pyplot as plt

font = cv2.FONT_HERSHEY_SIMPLEX
font1 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 23,
         }

Act = vision()
Expect = expectp()

plt.show()            
def ActualInfoCallback(msg):
    #rospy.loginfo("CV received Actual position: X:%f  Y:%f ", msg.x[0], msg.y[0])
    global Act
    Act = msg

def Position_To_Image(img):
    cv2.putText (img,( " Target:(%.2f,%.2f)"%(Act.x[0],Act.y[0])) ,(int(Act.x[0])*100-30,(1000-int(Act.y[0]*100))-50),font,0.7,(255,255,255),2)
    cv2.circle(img,(int (Act.x[0]*100),(1000-int(Act.y[0]*100))),20,(255,0,0),-1)
    for i in range (2,6):
        cv2.putText (img,( " ID:%d(%.2f,%.2f)"%(i,Act.x[i],Act.y[i])) ,(int(Act.x[i])*100-30,(1000-int(Act.y[i]*100))+50),font,0.7,(255,255,255),2)
        cv2.circle(img,(int (Act.x[i]*100),(1000-int(Act.y[i]*100))),20,(0,255,0),-1)

def Expect_To_Image(img):
    for i in range (2,6):
        #cv2.putText (img,( " ID:%d(%.2f,%.2f)"%(i,Expect.x[i],Expect.y[i])) ,(int(Expect.x[i]*100)-30,(1000-int(Expect.y[i]*100))+50),font,0.7,(255,255,255),2)
        cv2.circle(img,(int (Expect.x[i]*100),(1000-int(Expect.y[i]*100))),10,(0,0,255),-1)
        cv2.line(img,(int (Act.x[i]*100),(1000-int(Act.y[i]*100))),(int (Expect.x[i]*100),(1000-int(Expect.y[i]*100))),(0,0,255),2)

def ExpectInfoCallback(msg):
    rospy.loginfo("CV received Expected position x:%f y:%f", msg.x[0],msg.y[0])
    global Expect
    Expect = msg

def person_subscriber():
	# ROS节点初始化
    rospy.init_node('CV_sub', anonymous=True)
    rate = rospy.Rate(100) 

	# 创建一个Subscriber，订阅名为/person_info的topic，注册回调函数personInfoCallback
    rospy.Subscriber("/actual_info", vision, ActualInfoCallback)
    rospy.Subscriber("/expect_info", expectp, ExpectInfoCallback)
    #plt.plot(x,y,"ob",c='g') 
    plt.figure(figsize= (10,10))

    while not rospy.is_shutdown():
        global Act
        global Expect
        img2 =  np.zeros((1024,1024,3),np.uint8)
        Position_To_Image(img2)
        Expect_To_Image(img2)
        plt.imshow(img2)
        plt.show(block = False)
        plt.title("All The Robot's Position \n\n",font1) 
        plt.title("Green : Friends,Red :Target, Blue :Expect",loc='left') 
        plt.xlabel("x axis caption",font1) 
        plt.ylabel("y axis caption",font1) 
        plt.tick_params(labelsize=23)
        plt.yticks([1000,800,600,400,200,0],[0,2,4,6,8,10])
        plt.xticks([0,200,400,600,800,1000],[0,2,4,6,8,10])
        #plt.gca().invert_yaxis()
        plt.pause(0.001)
        plt.clf()
    rate.sleep()
    #rospy.spin()

if __name__ == '__main__':
    person_subscriber()
