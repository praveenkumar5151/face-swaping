import numpy as np
import cv2

import ImageProcessing

handImg = cv2.imread("C:/Users/User/Downloads/FaceSwap-master/FaceSwap-master/data/hand.png")
eyeImg = cv2.imread("C:/Users/User/Downloads/FaceSwap-master/FaceSwap-master/data/eye.png")
maskImg = cv2.imread("C:/Users/User/Downloads/FaceSwap-master/FaceSwap-master/data/mask.png")

#zmiana obrazka kolorowego na obrazek w skali szarosci
mask = np.mean(maskImg, axis=2)

eyeImg = ImageProcessing.colorTransfer(handImg, eyeImg, mask)
blendedImg = ImageProcessing.blendImages(eyeImg, handImg, mask)

cv2.imwrite("../eyeHandBlend.jpg", blendedImg)
