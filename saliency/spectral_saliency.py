# This file shows how to use the spectral saliency model from Hou & Zhang (2007), implemented in the OpenCV library. 
# There are two versions, a basic one and a fine grained one.

import cv2
from skimage import io, data_dir
import os
import numpy as np

file = os.path.join(data_dir, 'D:\Donnees\Mayoul.jpg') 
map = io.imread(file)

saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
(success, saliencyMap) = saliency.computeSaliency(map)
saliencyMap = (saliencyMap * 255).astype("uint8")

saliency2 = cv2.saliency.StaticSaliencyFineGrained_create()
(success, saliencyMap2) = saliency2.computeSaliency(map)
saliencyMap2 = (saliencyMap2 * 255).astype("uint8")

threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]



cv2.imshow("Image", map)
cv2.imshow("Output", threshMap)
cv2.waitKey(0)

io.imsave('D:\Donnees\Mayoul_saliency2.jpg',saliencyMap)