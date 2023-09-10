import cv2
import numpy as np
from cv_bridge import CvBridge

class CameraStream:
    def __init__(self, params):
        self.params = params
        self.image = None
        self.bridge = CvBridge()
        self.parse_params()

    def callback(self, img_msg):
        cv2_image = self.bridge.imgmsg_to_cv2(img_msg, "bgr8")
        self.image = self.translate_to_origin(cv2_image)

    def parse_params(self):    
        self.focal_length = self.params['intrinsics']['focal_length']
        self.principal_point = (self.params['intrinsics']['principal_point']['x'], self.params['intrinsics']['principal_point']['y'])
        k1 = self.params['intrinsics']['distortion']['radial']['k1']
        k2 = self.params['intrinsics']['distortion']['radial']['k2']
        k3 = self.params['intrinsics']['distortion']['radial']['k3']
        p1 = self.params['intrinsics']['distortion']['tangential']['p1']
        p2 = self.params['intrinsics']['distortion']['tangential']['p2']
        self.camera_matrix = np.array([[self.focal_length, 0, self.principal_point[0]],
                           [0, self.focal_length, self.principal_point[1]],
                           [0, 0, 1]])
        
        self.dist_coeffs = np.array([k1, k2, p1, p2, k3]) 
        self.x_shift = self.params['extrinsics']['pose']['translation']['x']
        self.y_shift = self.params['extrinsics']['pose']['translation']['y']
        self.z_shift = self.params['extrinsics']['pose']['translation']['z']

    def translate_to_origin(self, image):
        translation_matrix = np.float32([[1, 0, -int((self.x_shift * self.focal_length))], [0, 1, int((self.z_shift*self.focal_length))]])
        img = cv2.warpAffine(image, translation_matrix, (image.shape[1], image.shape[0]))
        return img
