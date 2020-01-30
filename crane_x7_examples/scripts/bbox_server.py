#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from darknet_ros_msgs.msg import BoundingBoxes
import hamburger

def DarknetBboxCallback(darknet_bboxs):
    bbox = darknet_bboxs.bounding_boxes[0]
    bbox_name = bbox.Class
    if bbox_name == 'paperplate':
        print(bbox.Class)

if __name__ == '__main__':
    try:
        if not rospy.is_shutdown():
            rospy.init_node('bbox_server', anonymous=True)
            rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, DarknetBboxCallback)  

            rospy.spin()

    except rospy.ROSInterruptException:
        pass
