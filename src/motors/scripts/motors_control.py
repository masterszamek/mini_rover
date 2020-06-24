#!/usr/bin/env python3 

import rospy
from motors.msg import Vel
import _thread
from adafruit_motorkit import MotorKit
import time
import math


velocity = Vel()
MOTORS = MotorKit()


def receive_velocity(data):
    global velocity
    velocity = data


def listener():
    rospy.init_node("motots")
    rospy.Subscriber("velocity", Vel, receive_velocity)


def set_velocity(x, y):
    global MOTORS
    y = y*(-1)
    print(x,y)
    if abs(x) < 0.1: x = 0.0
    if abs(y) < 0.1: y = 0.0
    MOTORS.motor1.throttle = y
    MOTORS.motor2.throttle = y
    MOTORS.motor3.throttle = y
    MOTORS.motor4.throttle = y

    if x > 0:
        MOTORS.motor1.throttle = MOTORS.motor1.throttle - (MOTORS.motor1.throttle*math.sin(x)*2)
        MOTORS.motor3.throttle = MOTORS.motor3.throttle - (MOTORS.motor3.throttle*math.sin(x)*2)
    elif x < 0:
        x = x*(-1)
        MOTORS.motor2.throttle = MOTORS.motor2.throttle - (MOTORS.motor2.throttle*math.sin(x)*2)
        MOTORS.motor4.throttle = MOTORS.motor4.throttle - (MOTORS.motor4.throttle*math.sin(x)*2)

def motors_stop():
    set_velocity(x=0, y=0)
    print("silniki STOP")
def motor_velocity():
    global velocity
    rate = rospy.Rate(10)
    try:
        while True:
            global velocity
            timer = (rospy.Time.now() - velocity.stamp)

            print(timer)
            print(time.time())
            print(type(rospy.Duration(nsecs = 150*(10**6))))
            if timer > rospy.Duration(nsecs = 150*(10**6)):
                motors_stop()
                continue
            print("dochodze")
            set_velocity(velocity.x, velocity.y)
            rate.sleep()
    except Exception as e:
        print(e)
        motors_stop()



if __name__ == "__main__":
    try:
        listener()
        _thread.start_new_thread(motor_velocity, ())
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
    