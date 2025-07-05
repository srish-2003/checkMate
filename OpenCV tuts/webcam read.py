import cv2
import numpy as np
from stack import stackImages


#read webcam
frameWidth=400
frameHeight=400

cap=cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
while True:
    success,img=cap.read()
    cv2.imshow("video",img)

    kernel = np.ones((5, 5), np.uint8)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 0)
    imgCanny = cv2.Canny(imgBlur, 60, 110)
    imgDilation = cv2.dilate(imgCanny, kernel, iterations=2)
    imgEroded = cv2.erode(imgDilation, kernel, iterations=2)

    imgArray = [[img, imgGray, imgBlur], [imgCanny, imgDilation, imgEroded]]
    imgStack = stackImages(0.5, imgArray)
    cv2.imshow("Image stack", imgStack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break