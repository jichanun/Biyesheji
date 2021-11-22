/**
 * 该例程将发布turtle1/cmd_vel话题，消息类型geometry_msgs::Twist
 */
 
#include <ros/ros.h>
#include <learn/Person.h>

int main(int argc, char **argv)
{
	// ROS节点初始化
	ros::init(argc, argv, "person_publisher");

	// 创建节点句柄
	ros::NodeHandle n;

	// 创建一个Publisher，发布名为/turtle1/cmd_vel的topic，消息类型为geometry_msgs::Twist，队列长度10
	ros::Publisher turtle_vel_pub = n.advertise<learn::Person>("/person_info", 10);

	// 设置循环的频率
	ros::Rate loop_rate(1);

	int count = 0;
	while (ros::ok())
	{
	    // 初始化geometry_msgs::Twist类型的消息
		learn::Person person_msg;
		person_msg.name ="Tom";
		person_msg.age = 18;
		person_msg.sex=learn::Person::male;

	    // 发布消息
		turtle_vel_pub.publish(person_msg);
		ROS_INFO("Publsh person info name %s ,  age  %d  ,sex:  %d  ", 
				person_msg.name.c_str(), person_msg.age,person_msg.sex);

	    // 按照循环频率延时
	    loop_rate.sleep();
	}

	return 0;
}