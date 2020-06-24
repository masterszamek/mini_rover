#!/usr/bin/env python3
from inputs import get_gamepad
import _thread
import csv
import time
import rospy
from joypad_driver.msg import Pad


def generate_gamepad_states_dict()-> dict:
    """Generate gamepad states dictionary  key: [human readable key, value]"""

   # f = open('/home/mlody/ros_wszystko/testowanie/src/joypad_driver/scripts/gamepad_keys.csv', "r")
    f = open("/home/pi/ros_wszystko/catkin_ws/src/joypad_driver/scripts/gamepad_keys.csv", "r")
    gamepad_states = {}

    with f:
        reader = csv.reader(f, delimiter=" ")
        for row in list(reader)[1:]:
            if row[0] == "MSC_SCAN" or row[0] == "SYN_REPORT" or row[0]=="SYN_DROPPED": continue 
            gamepad_states[row[0]] = [row[2], row[1]]
            
    return gamepad_states

def read_gamepad_states(gamepad_states):

    while 1:
        events = get_gamepad()
        for event in events:
            if event.code== "MSC_SCAN" or event.code == "SYN_REPORT" or event.code=="SYN_DROPPED": continue
            gamepad_states[event.code][1] = event.state

def print_gamepad_states(gamepad_states):

	for key in gamepad_states.keys():
		print(key, gamepad_states[key], sep=" -> ")


def prepare_dict_to_msg(gamepad_states):

	dic = {}
	for key in gamepad_states.keys():
		dic[gamepad_states[key][0]] = int(gamepad_states[key][1])
	return dic

def publish_gamepad_state(gamepad_states):

	pub = rospy.Publisher("gamepad_state_active", Pad, queue_size=10)
	rospy.init_node("gamepad_active", anonymous=False)
	rate = rospy.Rate(60)
	while not rospy.is_shutdown():
		msg = Pad(stamp=rospy.Time.now(), **prepare_dict_to_msg(gamepad_states))
		pub.publish(msg)
		rate.sleep()




if __name__ == "__main__":
	
	try:
		gamepad_states = generate_gamepad_states_dict()
		_thread.start_new_thread(read_gamepad_states, (gamepad_states, ))
		publish_gamepad_state(gamepad_states)
	except rospy.ROSInterruptException:
		pass

