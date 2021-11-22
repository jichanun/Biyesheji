/**
 * 该例程将发布turtle1/cmd_vel话题，消息类型geometry_msgs::Twist
 */
 
#include <ros/ros.h>
#include <learn/earphone.h>

int main(int argc, char **argv)
{
	// ROS节点初始化
	ros::init(argc, argv, "earphone_publisher");

	// 创建节点句柄
	ros::NodeHandle n;

	// 创建一个Publisher，发布名为/turtle1/cmd_vel的topic，消息类型为geometry_msgs::Twist，队列长度10
	ros::Publisher turtle_vel_pub = n.advertise<learn::earphone>("/earphone_message", 10);

	// 设置循环的频率
	ros::Rate loop_rate(1);

	int count = 0;
	while (ros::ok())
	{
	    // 初始化geometry_msgs::Twist类型的消息
		learn::earphone earphone1;
		earphone1.name ="Tom";
		earphone1.time = 18.1;
		earphone1.number=learn::earphone::left;

	    // 发布消息
		turtle_vel_pub.publish(earphone1);
		ROS_INFO("Publsh person info name %s ,  num  %d  ,time:  %.2f  ", 
				earphone1.name.c_str(), earphone1.number,earphone1.time);

	    // 按照循环频率延时
	    loop_rate.sleep();
	}

	return 0;
}