# 在各自相机使用函数中的预处理需要是三通道到三通道的

import cv2
import numpy as np
import math
import time
from struct import pack, unpack
import RPi.GPIO as GPIO
import signal
import atexit
from PIL import Image
import serial
from socket import *
from time import ctime
import binascii
import threading

def empty(a):
    pass

def color_filter(img, Lower, Upper, k_e, k_d):  # k_e为腐蚀处理的卷积核，k_d为膨胀处理的卷积核
    HSV_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    if Lower[0] > Upper[0]:
        mask1 = cv2.inRange(HSV_img, Lower, 180)
        mask2 = cv2.inRange(HSV_img, 0, Upper)
        mask = cv2.bitwise_and(mask1, mask2)
    else:
        mask = cv2.inRange(HSV_img, Lower, Upper)

        kernel_e = np.ones((k_e, k_e), np.uint8)  # 卷积核设置
        erosion = cv2.erode(mask, kernel_e, iterations=3)  # 腐蚀处理
        kernel_d = np.ones((k_d, k_d), np.uint8)  # 卷积核设置
        dilation = cv2.dilate(erosion, kernel_d, iterations=3)  # 膨胀处理

        img_maskcolor = dilation

    return img_maskcolor
#考虑到相机情况不同，在不同的相机函数中进行数据预处理


def accute_follow(img, lower, upper, k_e, k_d, sample_flag = 1): #使用双目相机进行特定区域的跟踪和测距
    img_binary = color_filter(img, lower, upper, k_e, k_d)
    img_binary_split = np.hsplit(img_binary,2)
    img_binary_1_split = img_binary_split[0]
    img_binary_2_split = img_binary_split[1]
    # 供参考的参数
    # img_binary_1_split = cv2.equalizeHist(img_binary_split[0]) 
    # img_binary_2_split = cv2.equalizeHist(img_binary_split[1]) 
    if sample_flag == 1:
        img_binary_1_split_down = cv2.pyrDown(img_binary_1_split)
        img_binary_2_split_down = cv2.pyrDown(img_binary_2_split)
    #是否进行下采样
    
    contours1, _ = cv2.findContours(img_binary_1_split_down, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    contours2, _ = cv2.findContours(img_binary_2_split_down, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    x_array_1 = []
    y_array_1 = []
    len_array_1 = list()
    x_array_2 = []
    y_array_2 = []
    len_array_2 = list()

    for contour1 in contours1:
        if (cv2.contourArea(contour1) > 50):
            M = cv2.moments(contour1)
            # print("len:" + str(len(approx)))
            # cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)  # 绘制轮廓线
            if (M['m00'] < 0.5):
                continue
            x = int(M['m10']/M['m00'])  # 廓线坐标
            y = int(M['m01']/M['m00'])  # 廓线坐标
            if (y < 360*(2-sample_flag)) & (y > 120*(2-sample_flag)) & (x > 120*(2-sample_flag)) & (x < 520*(2-sample_flag)) & (cv2.contourArea(contour1)>100):
                # print("y:" + str(y))
                # print("x:" + str(x))
                x_array_1.append(x)
                y_array_1.append(y)
                cv2.circle(img_binary_1_split_down, (x, y), 10, 2)

    x_array_1_ch=np.array(x_array_1)    
    # y_array_1_ch=np.array(y_array_1)
    # len_array_1_ch=np.array(len_array_1)

 

    for contour2 in contours2:
        if (cv2.contourArea(contour2 )>50):
            M = cv2.moments(contour2)
            # print("len:" + str(len(approx)))
            # cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)  # 绘制轮廓线
            if (M['m00'] < 0.5):
                continue
            x = int(M['m10']/M['m00'])  # 廓线坐标
            y = int(M['m01']/M['m00'])  # 廓线坐标
    
            if (y < 360*(2-sample_flag)) & (y > 120*(2-sample_flag)) & (x > 120*(2-sample_flag)) & (x < 520*(2-sample_flag)) & (cv2.contourArea(contour2)>100):
                # print("y:" + str(y))
                # print("x:" + str(x))
                x_array_2.append(x)
                y_array_2.append(y)
                cv2.circle(img_binary_2_split_down, (x, y), 10, 2)

    x_array_2_ch=np.array(x_array_2)
    # y_array_2_ch=np.array(y_array_2)
    # len_array_2_ch=np.array(len_array_2)
    print("len", len(x_array_1_ch))
    print("len", len(x_array_2_ch))
    cv2.imshow("bino1", img_binary_1_split_down)
    cv2.imshow("bino2", img_binary_2_split_down)
    if ((len(x_array_1_ch) - len(x_array_2_ch)) == 0) & (len(x_array_2_ch) != 0):
        if len(x_array_2_ch) == 1:
            for i in x_array_1_ch-x_array_2_ch:
                return 2000/i # 2000为比例系数，可根据不同环境来进行调整
        else:
            index_array = []
            for i in y_array_1:
                diff_array = []
                for j in y_array_2:
                    diff_array.append(abs(j-i))
                index_array.append(diff_array.index(min(diff_array)))
            for i,j in zip(x_array_1, index_array):
                return i-x_array_2[j]   #多目标多测量，编辑于7_23，version1
    else:
        return -1   #不对齐错误




def angle_control(img_middle, lower, upper, k_e, k_d): #鱼眼相机进行全角度角度粗略定位，判定顺序为中左右
    img_binary = color_filter(img_middle, lower, upper, k_e, k_d)
    # cv2.imshow("1",img_binary)
    contours, _ = cv2.findContours(img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    sign_angle = []
    angle = []
    for contour in contours :    
        approx  = cv2.approxPolyDP(contour , 0.008 * cv2.arcLength(contour , True), True)  # 计算轮廓线

        if (cv2.contourArea(contour )>50): # & (len(approx ) < 13) & (len(approx ) > 2):
            M = cv2.moments(contour)
            x = int(M['m10']/M['m00'])  # 廓线坐标
            y = int(M['m01']/M['m00'])  # 廓线坐标有待考察
            cv2.drawContours(img_binary, [approx ], 0, (0, 0, 0), 5)
            cv2.circle(img_binary, (x , y ), 10, (255, 0, 255), 2)
            # print(x)
            # print(y)
            angle1 = math.sqrt(math.pow(x-270,2)+math.pow(y-270,2))/270
            if angle1 <= 1:
                sign_angle.append(np.sign(x-270))
                angle.append(math.asin(angle1)/math.pi*180)

    if len(angle) == 0:     #这个是正面镜头看不到标记物，判定左侧，比较费劲但省速度
        return -1, 0        #第一个为状态位，第二个为信息位
    else:
        return 1, sign_angle[angle.index(min(angle))]*min(angle)

def send2algGH(offset, degree, R2_x, R2_y):

    offset_byte = pack('f', offset)  # 把float拆成4个字节值,返回列表
    degree_byte = pack('f', degree)  # 把float拆成4个字节值
    R2_x_byte = pack('f', R2_x)
    R2_y_byte = pack('f', R2_y)


    send_data = []

    send_data.append(chr(offset_byte[3]).encode('latin1'))  # 编码,追加到列表 以"latin1"编码可以编大于128的
    send_data.append(chr(offset_byte[2]).encode('latin1'))
    send_data.append(chr(offset_byte[1]).encode('latin1'))
    send_data.append(chr(offset_byte[0]).encode('latin1'))

    send_data.append(chr(degree_byte[3]).encode('latin1'))  # 编码成b,追加到列表
    send_data.append(chr(degree_byte[2]).encode('latin1'))
    send_data.append(chr(degree_byte[1]).encode('latin1'))
    send_data.append(chr(degree_byte[0]).encode('latin1'))

    send_data.append(chr(R2_x_byte[3]).encode('latin1'))
    send_data.append(chr(R2_x_byte[2]).encode('latin1'))
    send_data.append(chr(R2_x_byte[1]).encode('latin1'))
    send_data.append(chr(R2_x_byte[0]).encode('latin1'))

    send_data.append(chr(R2_y_byte[3]).encode('latin1'))
    send_data.append(chr(R2_y_byte[2]).encode('latin1'))
    send_data.append(chr(R2_y_byte[1]).encode('latin1'))
    send_data.append(chr(R2_y_byte[0]).encode('latin1'))


    i = 0
    ser.write(b'\xff\xff')  # 帧头
    while i < 16:
        ser.write(send_data[i])  # 发送数据
        i += 1

def send2algWB(offset, R2_x, R2_y):

    offset_byte = pack('f', offset)  # 把float拆成4个字节值,返回列表
    R2_x_byte = pack('f', R2_x)
    R2_y_byte = pack('f', R2_y)


    send_data = []

    send_data.append(chr(offset_byte[3]).encode('latin1'))  # 编码,追加到列表 以"latin1"编码可以编大于128的
    send_data.append(chr(offset_byte[2]).encode('latin1'))
    send_data.append(chr(offset_byte[1]).encode('latin1'))
    send_data.append(chr(offset_byte[0]).encode('latin1'))

    send_data.append(chr(R2_x_byte[3]).encode('latin1'))
    send_data.append(chr(R2_x_byte[2]).encode('latin1'))
    send_data.append(chr(R2_x_byte[1]).encode('latin1'))
    send_data.append(chr(R2_x_byte[0]).encode('latin1'))

    send_data.append(chr(R2_y_byte[3]).encode('latin1'))
    send_data.append(chr(R2_y_byte[2]).encode('latin1'))
    send_data.append(chr(R2_y_byte[1]).encode('latin1'))
    send_data.append(chr(R2_y_byte[0]).encode('latin1'))


    i = 0
    ser.write(b'\xff\xff')  # 帧头
    while i < 16:
        ser.write(send_data[i])  # 发送数据
        i += 1


def recv():
    data=np.zeros(15)
    count = ser.inWaiting()
    print(count)
    # count = 1
    if count != 0:
        print("1")
        rec = ser.read(57)
        #data = unpack("f",rec)
        for i in range(14):
            data[i]=rec[4*i+3]+rec[4*i+2]*(2**8)+rec[4*i+1]*(2**16)+rec[4*i]*(2**24)
            if i >1 :
                data[i] = data[i]/1000
        data[-1]=3
        #print(rec)
        
        #print("rec.back = " + str(rec[-1]))
        
        ser.flushInput()
    print('data:', data)
    return data

def CamOn(index, width, height):
    cap0 = cv2.VideoCapture(index)  # 正前方
    cap0.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # 设置宽度
    cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # 设置长度
    cap0.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
    cap0.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    return cap0

# 目标物自动跟随数据 70 90 100 255 40 145 3 5
cv2.namedWindow('HSV')
cv2.resizeWindow('HSV', 640, 240)
cv2.namedWindow('Kernels')
cv2.resizeWindow('Kernels', 320, 240)

cv2.createTrackbar('Hue min', 'HSV', 70, 179, empty)
cv2.createTrackbar('Hue max', 'HSV', 90, 179, empty)
cv2.createTrackbar('Sat min', 'HSV', 100, 255, empty)
cv2.createTrackbar('Sat max', 'HSV', 255, 255, empty)
cv2.createTrackbar('Val min', 'HSV', 40, 255, empty)
cv2.createTrackbar('Val max', 'HSV', 145, 255, empty)
cv2.createTrackbar('Kernel_e', 'HSV', 3, 10, empty)
cv2.createTrackbar('Kernel_d', 'HSV', 5, 10, empty)


ser = serial.Serial('/dev/ttyAMA0', 115200)  # ser = serial.Serial('/dev/ttyUSB0', 9600)//
if ser.isOpen == False:
    ser.open()


def Vision():

    depth_output = 0

    h_min = cv2.getTrackbarPos('Hue min', 'HSV')
    h_max = cv2.getTrackbarPos('Hue max', 'HSV')
    s_min = cv2.getTrackbarPos('Sat min', 'HSV')
    s_max = cv2.getTrackbarPos('Sat max', 'HSV')
    v_min = cv2.getTrackbarPos('Val min', 'HSV')
    v_max = cv2.getTrackbarPos('Val max', 'HSV')
    kernel_e = cv2.getTrackbarPos('Kernel_e', 'Kernels') # 腐蚀处理的卷积核
    kernel_d = cv2.getTrackbarPos('Kernel_d', 'Kernels') # 膨胀处理的卷积核
    # print(h_min, h_max, s_min, s_max, v_min, v_max)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    

    