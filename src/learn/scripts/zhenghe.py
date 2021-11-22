#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import serial #导入serial包
import rospy
import time

def node():
    rospy.init_node("serial_test") #初始化ros节点
    ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1) #打开串口, 端口号:"/dev/ttyUSB0". 波特率:9600. 延时等待1s
    if ser.isOpen(): #判断串口是否打开
        print("串口打开成功")
    else:
        print("串口打开失败")
        quit()
    while not rospy.is_shutdown():
        ser.write('hello')#发送hello
        time.sleep(1)#等待1s
        cnt = ser.inWaiting() #等待接受数据
        if cnt > 0 : #接受数据量大于0
            rev = ser.read(cnt) #读数据
            print(str(rev)) #打印

if __name__ == '__main__':
    try:
        node()
    except rospy.ROSInterruptException:
        pass

