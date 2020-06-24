#!/usr/bin/env python3 

import rospy
from joypad_driver.msg import Pad
from motors.msg import Vel

velocity_vector = [0.0, 0.0]


def motor_state(data):

	print(data.__str__)
	print("\n")

def calulcate_velocity(data):

	#print(data.V_LEFT_STICK, data.H_LEFT_STICK)
	global velocity_vector
	velocity_vector = [
		(data.H_RIGHT_STICK-128)/(-128), 
		(data.V_LEFT_STICK-128)/(-128)
	]
	print(velocity_vector)
def listener():

	rospy.init_node("drive_state")
	#rospy.Subscriber("gamepad_state_passive", Pad, motor_state)
	rospy.Subscriber("gamepad_state_active", Pad, calulcate_velocity)


def publish_velocity():
	global velocity_vector
	pub = rospy.Publisher("velocity", Vel, queue_size=10)
	rospy.init_node("drive_state", anonymous=False)
	rate = rospy.Rate(60)
	while not rospy.is_shutdown():
		msg = Vel(stamp=rospy.Time.now(), x=velocity_vector[0], y=velocity_vector[1])
		pub.publish(msg)
		rate.sleep()


if __name__ == "__main__":
	try:
		listener()
		
		publish_velocity()
	except rospy.ROSInterruptException:
		pass


