#!/usr/bin/env python
import roslib; roslib.load_manifest('aiden')
import sys
import rospy


from aiden.srv import *
from sensor_msgs.msg import Image
from zed_interfaces.msg import Object
from zed_interfaces.msg import ObjectsStamped
from std_msgs.msg import String



obj_data = [0, 0, [1,1, 2]]

# Hand node communication function
def hand_com(x, y, z):
	rospy.wait_for_service("hand_srv")
	try: 
		move_server = rospy.ServiceProxy("hand_srv", Messages)
		data = move_server(x, y, z)
		return data.report
	except rospy.ServiceException as e:
		return e

# Move node communication function
def move_com(x, y, z):
	global pub
	str  = "{} {} {}".format(x, y, z)
	pub.publish(String(str))
	print(str)

# Received data processing function
def callback(data):
	global obj_data
	obj_data = []
	rospy.loginfo("***** New Object *****")
	for i in range(0, len(data.objects)):
		if data.objects[i].lable == "Person":
			obj_data.append([data.objects[i].label, data.objects[i].label_id, [data.objects[i].position[0], data.objects[i].position[1], data.objects[i].position[2]], data.objects[i].confidence, data.objects[i].tracking_state ])
			break

def main():
	#rospy.Subscriber("/zed2/zed_node/obj_det/objects", ObjectsStamped, callback)
	global obj_data
	if obj_data:
		if obj_data[2][2]>1:
			move_com(obj_data[2][0], obj_data[2][1], obj_data[2][2])
		else:
			rep = hand_com(obj_data[2][0], obj_data[2][1], obj_data[2][2])
			if rep!="done":
				print("Manipulator error: {}".format(rep) )
			else:
				print("Mission completed")
	rospy.spin()

if __name__ == '__main__':
	pub = rospy.Publisher('main_node_move', String)
	rospy.init_node('main_node')
	
	main()



########################################################################################################
#	for i in range(0, len(data.objects)):
#		if data.objects[i].lable_id == -1:
#			continue
#		obj_data.append([data.objects[i].label, data.objects[i].label_id, [data.objects[i].position[0], data.objects[i].position[1], #data.objects[i].position[2]], data.objects[i].confidence, data.objects[i].tracking_state ]) # 0: lable - 1: ID - 2:[x,y,z] - 3: confidence - 4: t_s
########################################################################################################
