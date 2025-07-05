# import numpy as np
# import cv2
#
#
# def stackImages(scale,imgArray):
#     rows=len(imgArray)
#     cols=len(imgArray[0])
#     rowsAvailable=isinstance(imgArray[0],list)
#     width=imgArray[0][0].shape[1]
#     height=imgArray[0][0].shape[0]
#     if rowsAvailable:
#         for x in range(0,rows):
#             for y in range(0,cols):
#                 if imgArray[x][y].shape[:2]==imgArray[0][0].shape[:2]:
#                     imgArray[x][y]=cv2.resize(imgArray[x][y],(0,0),None,scale,scale)
#                 else:
#                     imgArray[x][y] = cv2.resize(imgArray[x][y],(imgArray[0][0].shape[1],imgArray[0][0].scale[0]),None,scale,scale)
#                 if len(imgArray[x][y].shape)==2:
#                     imgArray[x][y]=cv2.cvtColor((imgArray[x][y]),cv2.COLOR_GRAY2BGR)
#         imgBlank=np.zeros((height,width,3),np.uint8)
#         hor=[imgBlank]*rows
#         hor_con=[imgBlank]*rows
#         for x in range(0,rows):
#             hor[x]=np.hstack(imgArray[x])
#         ver=np.vstack(hor)
#
#     else:
#         for x in range(0,rows):
#             if imgArray[x].shape[:2]==imgArray[0].shape[:2]:
#                 imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
#             else:
#                 imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].scale[0]), None,scale, scale)
#             if len(imgArray[x].shape) == 2:
#                 imgArray[x] = cv2.cvtColor((imgArray[x]), cv2.COLOR_GRAY2BGR)
#         hor=np.hstack(imgArray)
#         ver=hor
#     return ver
#


import numpy as np
import cv2


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0]) if isinstance(imgArray[0], list) else 1
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1] if rowsAvailable else imgArray[0].shape[1]
    height = imgArray[0][0].shape[0] if rowsAvailable else imgArray[0].shape[0]

    if rowsAvailable:
        for x in range(rows):
            for y in range(cols):
                if imgArray[x][y].shape[:2] == (height, width):
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), fx=scale, fy=scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (width, height))
                if len(imgArray[x][y].shape) == 2:  # Convert grayscale to BGR
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)

        imgBlank = np.zeros((int(height * scale), int(width * scale), 3), np.uint8)
        hor = [imgBlank] * rows
        for x in range(rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(rows):
            if imgArray[x].shape[:2] == (height, width):
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), fx=scale, fy=scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (width, height))
            if len(imgArray[x].shape) == 2:  # Convert grayscale to BGR
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)

        ver = np.hstack(imgArray)

    return ver


