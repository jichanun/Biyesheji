/**
 * 该例程将订阅/turtle1/pose话题，消息类型turtlesim::Pose
 */
 
#include <ros/ros.h>
#include "learn/earphone.h"

// 接收到订阅的消息后，会进入消息回调函数
void personCallback(const learn::earphone::ConstPtr& msg)
{
    // 将接收到的消息打印出来
    ROS_INFO("subcribe person info: name:%s, num:%d,time:%.2f", msg->name.c_str(), msg->number,msg->time);
}

int main(int argc, char **argv)
{
    // 初始化ROS节点
    ros::init(argc, argv, "earphone_subscriber");

    // 创建节点句柄
    ros::NodeHandle n;

    // 创建一个Subscriber，订阅名为/turtle1/pose的topic，注册回调函数poseCallback
    ros::Subscriber person_info_sub = n.subscribe("/earphone_message", 10, personCallback);

    // 循环等待回调函数，死循环
    ros::spin();

    return 0;
}