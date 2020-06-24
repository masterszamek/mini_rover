#!/usr/bin/env python3 


import rospy
from motors.msg import Motors_rpm
import json
import serial

ser =  serial.Serial("/dev/ttyS0", 250000)

def talker():
    pub = rospy.Publisher("motors_rpm", Motors_rpm, queue_size=10)
    rospy.init_node("pi", anonymous=True)
    rate = rospy.Rate(1000)
    while not rospy.is_shutdown():
        try:
            data = ser.readline()
            data = data.decode("utf-8")[:-1]
            parsed = json.loads(data)
            print(parsed)
            
            pub.publish(FL_motor=parsed["FL"]["rpm"], 
                    BL_motor=parsed["BL"]["rpm"], 
                    FR_motor=parsed["FR"]["rpm"], 
                    BR_motor=parsed["BR"]["rpm"]
                    )
            rate.sleep()
        except Exception as e:
            continue

if __name__ == "__main__":
    try:
        talker()
    except rospy.ROSInterruptException as e:
        print(e)