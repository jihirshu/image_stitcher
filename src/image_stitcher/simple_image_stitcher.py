import cv2
import imutils
import numpy as np
from cv_bridge import CvBridge
from threading import Lock
from image_stitcher.camera_stream import CameraStream

class MultiImageStitcher:
    def __init__(self, 
                camera_stream_1: CameraStream, 
                camera_stream_2: CameraStream, 
                camera_stream_3: CameraStream, 
                publish_review_image):

        self.camera_stream_1 = camera_stream_1
        self.camera_stream_2 = camera_stream_2
        self.camera_stream_3 = camera_stream_3
        self.publish_review_image = publish_review_image
        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.lock = Lock()
        self.bridge = CvBridge()
        self.stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()

    def synced_callback(self, image1, image2, image3):
        with self.lock:
            self.camera_stream_1.callback(image1)
            self.camera_stream_2.callback(image2)
            self.camera_stream_3.callback(image3)

            result = self.stitch_stream()
            self.publish_review_image(self.bridge.cv2_to_imgmsg(result))

    def stitch_stream(self):
        (status, stitched_image) = self.stitcher.stitch([self.camera_stream_1.image, 
                                                        self.camera_stream_2.image, 
                                                        self.camera_stream_3.image])

        if status == cv2.Stitcher_OK:
            result = stitched_image  
        else:
            result = np.hstack((self.camera_stream_1.image, 
                                self.camera_stream_2.image, 
                                self.camera_stream_3.image))        

        return result