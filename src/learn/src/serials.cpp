//serial_port.cpp
#include <ros/ros.h>
#include <serial/serial.h>
#include <iostream>
#include "serials.hpp"
#include "learn/vision.h"
#include "learn/expectp.h"
#include"time.h"
#define HAS_STM32  1 


ToRosUnion ReceiveData,TransmitData;
void ExpectCallback(const learn::expectp::ConstPtr& msg)
{
    // 将接收到的消息打印出来
    //ROS_INFO("subcribe person info: name:%s, age:%d,sex:%d", msg->name.c_str(), msg->age,msg->sex);
    TransmitData.vars.data0=20000;
    TransmitData.vars.data1=0;
    for (int i =0;i<7;i++){
        TransmitData.vars.px[i]=msg->x[i];
        TransmitData.vars.py[i]=msg->y[i];
    }
    TransmitData.vars.status=2;
    ROS_INFO ("The expeted position of all the robots are:");
    for (int i =0;i<7;i++)
        ROS_INFO ("Robot ID : %d x: %.2f ,y : %.2f ",i, msg->x[i],msg->y[i]);
    #if HAS_STM32
    #else
        ToRosUnion temp;
    for (int i =1;i<6;i++)
    {    
        temp.vars.px[i]=TransmitData.vars.px[i]-ReceiveData.vars.px[i];
        temp.vars.py[i]=TransmitData.vars.py[i]-ReceiveData.vars.py[i];
        if (i == 2||i ==5)
        {
            temp.vars.px[i]*=1.5;
            temp.vars.py[i]*=1.5;
        }

        int num = rand() % 200 -99;


        ReceiveData.vars.px[i]+=0.005*temp.vars.px[i]+(float)num/2000;
        ReceiveData.vars.py[i]+=0.01*temp.vars.py[i]+(float)num/2000;

        //乘i表示每个机器人的运动速度不尽相同，这样不会使机器人叠加到一起
    }
    #endif
}
uint8_t InitFlag=0;

int main(int argc, char** argv)
{
    ros::init(argc, argv, "serial_port");
    //创建句柄（虽然后面没用到这个句柄，但如果不创建，运行时进程会出错）
    ros::NodeHandle f;
    ros::NodeHandle e;
    ros::Subscriber Expect = e.subscribe("/expect_info", 50, ExpectCallback);
	ros::Publisher Acutal = f.advertise<learn::vision>("/actual_info", 50);
    //创建一个serial类
    serial::Serial sp;
    //创建timeout
    serial::Timeout to = serial::Timeout::simpleTimeout(100);
    //设置要打开的串口名称
    sp.setPort("/dev/ttyACM0");
    //设置串口通信的波特率
    sp.setBaudrate(115200);
    //串口设置timeout
    sp.setTimeout(to);
    srand((unsigned int)time(0));
 #if HAS_STM32
    try
    {
        //打开串口
        sp.open();
    }
    catch(serial::IOException& e)
    {
        ROS_ERROR_STREAM("Unable to open port.");
        return -1;
    }
    
    //判断串口是否打开成功
    if(sp.isOpen())
    {
        ROS_INFO_STREAM("/dev/ttyUSB0 is opened.");
    }
    else
    {
        return -1;
    }

#else
    ROS_INFO_STREAM("DEBUG MODE ");
#endif

    ros::Rate loop_rate(5);
    while(ros::ok())
    {
        //获取缓冲区内的字节数
        size_t n = sp.available();
#if  HAS_STM32
        if(n!=0)
        {
            uint8_t buffer[68];
            uint8_t sendbuf[68];
            //读出数据
            n = sp.read(buffer, n);
            for (int i =0;i<65;i++)
                ReceiveData.buf[i]=buffer[i];
            
            printf("Received from STM32 : DATA0 :%.2f  data1 %.2f\n ",ReceiveData.vars.data0,ReceiveData.vars.data1);
            for (int i=0;i<7;i++)
            {
                ReceiveData.vars.px[i]/=1000;
                ReceiveData.vars.py[i]/=1000;
                printf("Position NUMBER %d :  X :%.2f  Y :%.2f\n ",i,ReceiveData.vars.px[i],ReceiveData.vars.py[i]);
            }
            printf("status is %d \n",ReceiveData.vars.status);

            //向节点发送实际位置
            learn::vision Act;
            for (int i=0;i<7;i++){
                Act.x[i]=ReceiveData.vars.px[i];
                Act.y[i]=ReceiveData.vars.py[i];
                
            }
            Acutal.publish(Act);

            //写入数据
            for (int k=0;k<65;k++)
                sendbuf[k]=TransmitData.buf[k];
            sp.write(sendbuf, 65);

            /*
            for(int i=0; i<n; i++)
            {
                //16进制的方式打印到屏幕
                std::cout << std::hex << (buffer[i] & 0xff) << " ";
            }
            std::cout << std::endl;
            */


            //把数据发送回去
        }
#else
        ReceiveData.vars.data0=300;
            learn::vision Act;
            if (!InitFlag){//调试时初始化所有机器人
                ReceiveData.vars.px[0]=5;ReceiveData.vars.py[0]=8;//设定目标位置
                ReceiveData.vars.px[2]=4.5;ReceiveData.vars.py[2]=2;
                ReceiveData.vars.px[3]=3;ReceiveData.vars.py[3]=1;
                ReceiveData.vars.px[4]=6;ReceiveData.vars.py[4]=1;
                ReceiveData.vars.px[5]=4.5;ReceiveData.vars.py[5]=0;
                InitFlag=1;
            }
            for (int i=0;i<6;i++){
                Act.x[i]=ReceiveData.vars.px[i];
                Act.y[i]=ReceiveData.vars.py[i];
                
            }
            printf("All actual position are:\n");
            for (int k=0;k<6;k++)
                printf("Number : %d  , X:  %.2f ,   Y :  %.2f\n", k , Act.x[k],Act.y[k]);
            Acutal.publish(Act);
#endif

        ros::spinOnce();
        loop_rate.sleep();
    }
    
    //关闭串口
    sp.close();
 
    return 0;
}
