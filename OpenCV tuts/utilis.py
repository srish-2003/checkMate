from operator import truediv

import numpy as np
import cv2
from numpy.core.fromnumeric import argmin


def rectContours(contours):
    rectCon=[]
    for i in contours:
        area=cv2.contourArea(i)
        #print(area)
        if(area>100):
            peri=cv2.arcLength(i,True)
            approx=cv2.approxPolyDP(i,0.02*peri,True)
            #print("corner points", len(approx))
            if len(approx)==4:
                rectCon.append(i)

    #print(rectCon)
    rectCon=sorted(rectCon,key=cv2.contourArea,reverse=True)
    return rectCon

def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True)
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True)
    return approx

def reorder(myPoints):

    myPoints=myPoints.reshape((4,2))
    myPointsNew=np.zeros((4,1,2),np.int32)
    add=myPoints.sum(1)
    # print(myPoints)
    # print(add)
    myPointsNew[0]=myPoints[np.argmin(add)]
    myPointsNew[3]=myPoints[np.argmax(add)]
    diff=np.diff(myPoints,axis=1)
    myPointsNew[1]=myPoints[np.argmin(diff)]
    myPointsNew[2]=myPoints[np.argmax(diff)]
    # print(diff)

    return myPointsNew


def splitBoxes(img, skip_left=100,skip_right=30):
    """
    Splits the input image into smaller boxes after skipping a portion on the left.

    Parameters:
        img (numpy.ndarray): The input image to split.
        skip_left (int): The number of pixels to skip from the left.

    Returns:
        list: A list of smaller boxes.
    """
    # Skip the left portion by cropping the image
    img_cropped = img[:, skip_left:img.shape[1] - skip_right]

    # Split the cropped image into 5 rows
    rows = np.vsplit(img_cropped, 5)
    boxes = []

    # Split each row into 5 columns
    for r in rows:
        cols = np.hsplit(r, 5)
        for box in cols:
            boxes.append(box)

    return boxes

def showAnswers(img,myIndex,grading,answers,questions,options):
    secW=int(img.shape[1]/questions)
    secH=int(img.shape[0]/options)

    for x in range(0,questions):
        myAnswer=myIndex[x]
        cX=(myAnswer*secW)+secW//2
        cY=(x*secH)+secH//2

        if grading[x]==1:
            myColor=(0,255,0)
        else:
            myColor=(0,0,255)

        cv2.circle(img,(cX,cY),35,(myColor),cv2.FILLED)

    return img
