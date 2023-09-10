#!/usr/bin/env python3

import json
import rospy
import message_filters
from sensor_msgs.msg import Image
from image_stitcher.camera_stream import CameraStream
from image_stitcher.simple_image_stitcher import MultiImageStitcher

def main():
    rospy.init_node('image_stitcher_node')
    rospy.loginfo("Initializing image stitcher node")

    image_1_topic = rospy.get_param("~image_1_topic", "/platypus/camera_1/dec/manual_white_balance")
    image_2_topic = rospy.get_param("~image_2_topic", "/platypus/camera_2/dec/manual_white_balance")
    image_3_topic = rospy.get_param("~image_3_topic", "/platypus/camera_3/dec/manual_white_balance")
    camera_params_json_path = rospy.get_param("~camera_json_path", "intrinsics_extrinsics.json")
    review_publish_topic = rospy.get_param("~review_publish_topic", "/review")
    
    review_image_publisher = rospy.Publisher(review_publish_topic, Image, queue_size=1)
    f = open(camera_params_json_path)
    camera_params = json.load(f)
    camera_1_config = CameraStream(camera_params['camera_1'])
    camera_2_config = CameraStream(camera_params['camera_2'])
    camera_3_config = CameraStream(camera_params['camera_3'])
    multi_image_stitcher = MultiImageStitcher(camera_1_config,
                                            camera_2_config,
                                            camera_3_config,
                                            review_image_publisher.publish)

    image_sub1 = message_filters.Subscriber(image_1_topic, Image)
    image_sub2 = message_filters.Subscriber(image_2_topic, Image)
    image_sub3 = message_filters.Subscriber(image_3_topic, Image)

    ts = message_filters.TimeSynchronizer([image_sub3, image_sub2, image_sub1], 3)
    ts.registerCallback(multi_image_stitcher.synced_callback)
    rospy.loginfo("Image stitcher node spinning ")
    rospy.spin()


if __name__ == '__main__':
    main()