#!/usr/bin/env python
# -*- coding: utf-8 -*-

###这个文件作为串口通信与定位信息的中转站，
#从串口接受机器人实际位置，pub给三个（或1个）解算器和1个CV
#从解算器中sub机器人的期望位置，发送给1个基站

#该函数定时运行，定时向机器人进行通信

#仿真说明：使用某种方式替换掉串口模块，在Expect回调函数中更新机器人的实际位置


from rosgraph.names import anonymous_name
import rospy
from learn.msg import earphone
from learn.msg import vision
from learn.msg import expectp
import math
import numpy as np
from struct import pack, unpack
import serial #导入serial包

Actual_test = vision()
Expect_test = expectp()
def Simulation_test():
    Error_test = vision()
    Actual_out = vision()
    for i in range (5):
        Error_test.x[i]= Expect_test.x[i] - Actual_test.x[i]
        Error_test.y[i]= Expect_test.y[i] - Actual_test.y[i]

        Actual_out.x[i]=Actual_test.x[i]+Error_test.x[i]*0.3
        Actual_out.y[i]=Actual_test.y[i]+Error_test.y[i]*0.3
    return Actual_out

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1) #打开串口, 端口号:"/dev/ttyUSB0". 波特率:9600. 延时等待1s

def node():

    print("serial:::::::::::")
    if ser.isOpen(): #判断串口是否打开
        print("串口打开成功")
    else:
        print("串口打开失败")
        quit()

        
def send2algGH(R1_x, R1_y, R2_x, R2_y,R3_x, R3_y, R4_x, R4_y):

    R1_x_byte = pack('f', R1_x)  # 把float拆成4个字节值,返回列表
    R1_y_byte = pack('f', R1_y)  # 把float拆成4个字节值
    R2_x_byte = pack('f', R2_x)
    R2_y_byte = pack('f', R2_y)
    R3_x_byte = pack('f', R3_x)  # 把float拆成4个字节值,返回列表
    R3_y_byte = pack('f', R3_y)  # 把float拆成4个字节值
    R4_x_byte = pack('f', R4_x)
    R4_y_byte = pack('f', R4_y)


    send_data = []

    send_data.append(chr(R1_x_byte[3]).encode('latin1'))  # 编码,追加到列表 以"latin1"编码可以编大于128的
    send_data.append(chr(R1_x_byte[2]).encode('latin1'))
    send_data.append(chr(R1_x_byte[1]).encode('latin1'))
    send_data.append(chr(R1_x_byte[0]).encode('latin1'))

    send_data.append(chr(R1_y_byte[3]).encode('latin1'))  # 编码成b,追加到列表
    send_data.append(chr(R1_y_byte[2]).encode('latin1'))
    send_data.append(chr(R1_y_byte[1]).encode('latin1'))
    send_data.append(chr(R1_y_byte[0]).encode('latin1'))

    send_data.append(chr(R2_x_byte[3]).encode('latin1'))
    send_data.append(chr(R2_x_byte[2]).encode('latin1'))
    send_data.append(chr(R2_x_byte[1]).encode('latin1'))
    send_data.append(chr(R2_x_byte[0]).encode('latin1'))

    send_data.append(chr(R2_y_byte[3]).encode('latin1'))
    send_data.append(chr(R2_y_byte[2]).encode('latin1'))
    send_data.append(chr(R2_y_byte[1]).encode('latin1'))
    send_data.append(chr(R2_y_byte[0]).encode('latin1'))

    send_data.append(chr(R3_x_byte[3]).encode('latin1'))  # 编码,追加到列表 以"latin1"编码可以编大于128的
    send_data.append(chr(R3_x_byte[2]).encode('latin1'))
    send_data.append(chr(R3_x_byte[1]).encode('latin1'))
    send_data.append(chr(R3_x_byte[0]).encode('latin1'))

    send_data.append(chr(R3_y_byte[3]).encode('latin1'))  # 编码成b,追加到列表
    send_data.append(chr(R3_y_byte[2]).encode('latin1'))
    send_data.append(chr(R3_y_byte[1]).encode('latin1'))
    send_data.append(chr(R3_y_byte[0]).encode('latin1'))

    send_data.append(chr(R4_x_byte[3]).encode('latin1'))
    send_data.append(chr(R4_x_byte[2]).encode('latin1'))
    send_data.append(chr(R4_x_byte[1]).encode('latin1'))
    send_data.append(chr(R4_x_byte[0]).encode('latin1'))

    send_data.append(chr(R4_y_byte[3]).encode('latin1'))
    send_data.append(chr(R4_y_byte[2]).encode('latin1'))
    send_data.append(chr(R4_y_byte[1]).encode('latin1'))
    send_data.append(chr(R4_y_byte[0]).encode('latin1'))
    print("len is %d"%len(send_data))
    #for  i in range(len(send_data)):
     #   ser.write(send_data[i])
    ser.write(send_data)#看看这里会不会产生16个中断



Actual =  rospy.Publisher('/actual_info',vision,queue_size=50)
def ExpectInfoCallback(msg):
    rospy.loginfo("Serial received  expect position Info: x:%f  y:%f", msg.x[0], msg.y[0])
    send2algGH( msg.x[0], msg.y[0], msg.x[1], msg.y[1], msg.x[2], msg.y[2], msg.x[3], msg.y[3])#串口通信
    rospy.loginfo("Serial sended to STM32 ")




def recv():
    data=np.zeros(15)

    print("111111111111111111")
    rec = ser.read(57)
    #data = unpack("f",rec)
    for i in range(14):
        data[i]=rec[4*i+3]+rec[4*i+2]*(2**8)+rec[4*i+1]*(2**16)+rec[4*i]*(2**24)
        if i >1 :
            data[i] = data[i]/1000
    #print(rec)
    
    #print("rec.back = " + str(rec[-1]))
    
    ser.flushInput()
    print('data:', data)
    return data

def person_subscriber():
	# ROS节点初始化
    rospy.init_node('ear_sub', anonymous=True)
    rate = rospy.Rate(1) 
	# 创建一个Subscriber，订阅名为/person_info的topic，注册回调函数personInfoCallback
    rospy.Subscriber("/expect_info", expectp,ExpectInfoCallback)

    #node()#开启节点


    while not rospy.is_shutdown():
        #ser.write('h'.encode())#发送hello
        print("hello")
        cnt = ser.inWaiting() #等待接受数据
        if cnt > 0 : #接受数据量大于0
            rev = ser.read(cnt) #读数据
            print(len(rev)) #打印长度
            data1= recv()#解码

            Act=vision()
            rospy.loginfo("All Actual position Received :::::/r/n  ")
            for i in range(0,6):
                Act.x[i]=data1[i*2+2]
                Act.y[i]=data1[i*2+3]#六个机器人的坐标集
                rospy.loginfo("Number  %d   : X=%f , Y=%f /n", i,Act.x[i],Act.y[i])

            #Act=Simulation_test()#数据仿真

            Actual.publish(Act)            #发布消息



        rate.sleep()#延时



    rospy.spin()

if __name__ == '__main__':
    person_subscriber()


