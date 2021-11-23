#ifndef __serials__
#define __serials__
#include <stdlib.h>
#include <ros/ros.h>
#include <string.h>

 union ToRosUnion

{
	/* data */
	uint8_t buf [57];
	struct 
	{
		/* data */
		float data0;
		float data1;
		float px[6];
		float py[6];
		uint8_t status ; 
	}vars;
	
};


#endif