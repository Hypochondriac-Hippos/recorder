#!/usr/bin/env python2

"""
Dump the stream of images from to robot camera to a video file for later analysis.

The video is saved to ~/Videos/353_recordings/start datetime in UTC.avi (datetime formatted per ISO 8601)

Subscribes to /R1/pi_camera/image_raw for image data.
"""

import datetime
import os

import cv_bridge
import cv2
import rospy
from sensor_msgs import msg

import util
from video import VideoWriter

bridge = cv_bridge.CvBridge()


def record_with(writer):
    """Closure on the VideoWriter object to allow cleanup"""

    def record(ros_image):
        image = bridge.imgmsg_to_cv2(ros_image, "bgr8")
        writer.write(image)

    return record


def ensure_directory(directory):
    if not os.path.isdir(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            raise OSError(
                "File exists at {}. Can't set up a directory there.".format(directory)
            )


if __name__ == "__main__":
    now = datetime.datetime.utcnow()
    now = now.replace(microsecond=0)  # Microseconds are unnecessarily precise

    output_directory = os.path.expanduser("~/Videos/353_recordings")
    ensure_directory(output_directory)
    output_file = os.path.join(output_directory, "{}.avi".format(now.isoformat()))

    rospy.init_node("license_detector", anonymous=True)
    with VideoWriter(
        output_file, cv2.VideoWriter_fourcc(*"XVID"), 20.0, util.camera_resolution
    ) as writer:
        subscriber = rospy.Subscriber(
            util.topics["images"], msg.Image, record_with(writer)
        )
        rospy.spin()
