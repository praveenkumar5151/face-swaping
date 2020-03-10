import dlib
import cv2
import numpy as np

import models
import NonLinearLeastSquares
import ImageProcessing

from drawing import *

import FaceRendering
import utils

print ("Press T to draw the keypoints and the 3D model")
print ("Press R to start recording to a video file")

predictor_path = "C:/Users/User/Downloads/FaceSwap-master/FaceSwap-master/shape_predictor_68_face_landmarks.dat"
image_name = "C:/Users/User/Downloads/FaceSwap-master/FaceSwap-master/data/jolie.jpg"

maxImageSizeForDetection = 320

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("C:/projects/landmark/shape_predictor_68_face_landmarks.dat")
mean3DShape, blendshapes, mesh, idxs3D, idxs2D = utils.load3DFaceModel("C:/Users/User/Downloads/FaceSwap-master/FaceSwap-master/candide.npz")

projectionModel = models.OrthographicProjectionBlendshapes(blendshapes.shape[0])

modelParams = None
lockedTranslation = False
drawOverlay = False
cap = cv2.VideoCapture(0)
writer = None
cameraImg = cap.read()[1]

textureImg = cv2.imread(image_name)
textureCoords = utils.getFaceTextureCoords(textureImg, mean3DShape, blendshapes, idxs2D, idxs3D, detector, predictor)
renderer = FaceRendering.FaceRenderer(cameraImg, textureImg, textureCoords, mesh)

while True:
    cameraImg = cap.read()[1]
    shapes2D = utils.getFaceKeypoints(cameraImg, detector, predictor, maxImageSizeForDetection)

    if shapes2D is not None:
        for shape2D in shapes2D:
            
            modelParams = projectionModel.getInitialParameters(mean3DShape[:, idxs3D], shape2D[:, idxs2D])

            modelParams = NonLinearLeastSquares.GaussNewton(modelParams, projectionModel.residual, projectionModel.jacobian, ([mean3DShape[:, idxs3D], blendshapes[:, :, idxs3D]], shape2D[:, idxs2D]), verbose=0)

            
            shape3D = utils.getShape3D(mean3DShape, blendshapes, modelParams)
            renderedImg = renderer.render(shape3D)

            
            mask = np.copy(renderedImg[:, :, 0])
            renderedImg = ImageProcessing.colorTransfer(cameraImg, renderedImg, mask)
            cameraImg = ImageProcessing.blendImages(renderedImg, cameraImg, mask)
       

            
            if drawOverlay:
                drawPoints(cameraImg, shape2D.T)
                drawProjectedShape(cameraImg, [mean3DShape, blendshapes], projectionModel, mesh, modelParams, lockedTranslation)

    if writer is not None:
        writer.write(cameraImg)

    cv2.imshow('image', cameraImg)
    key = cv2.waitKey(1)

    if key == 27:
        break
    if key == ord('t'):
        drawOverlay = not drawOverlay
    if key == ord('r'):
        if writer is None:
            print ("Starting video writer")
            fourcc = cv2.cv.CV_FOURCC(*'XVID')  
            videoOut = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))
            if writer.isOpened():
                print ("Writer succesfully opened")
            else:
                writer = None
                print ("Writer opening failed")
        else:
            print ("Stopping video writer")
            writer.release()
            writer = None










            
