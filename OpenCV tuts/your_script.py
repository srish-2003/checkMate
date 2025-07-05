import cv2
import numpy as np
import stack
import utilis


path='assets/3.jpg'
pathB='assets/WhatsApp Image 2024-11-24 at 12.02.38_1e035c48.jpg'
height,width=600,600
questions=5
options=5
##answers = np.array(list(map(int, input("Enter answers separated by spaces: ").split())))
answers=[1,1,1,1,1]

####################################################################################################
webcamFeed=True
cameraNo=0

cap=cv2.VideoCapture(cameraNo)
cap.set(10,150)

while True:
    if webcamFeed: success, img=cap.read()
    else:
        img=cv2.imread(path)

    img=cv2.resize(img,(width,height))
    imgBlank=cv2.resize(cv2.imread(pathB),(width,height))
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(5,5),0)
    imgCanny=cv2.Canny(imgBlur,10,50)
    imgContours=img.copy()
    imgContourBiggest=img.copy()

    ###############################################################
    try:
        contours, hierarchy=cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(imgContours,contours,-1,(0,255,0),6)
        rectCon=utilis.rectContours(contours)
        biggestContour=utilis.getCornerPoints(rectCon[0])
        #print(len(biggestContour))##gives numbers of points in the biggest contour
        gradeContour=utilis.getCornerPoints(rectCon[1])
        # print(biggestContour) prints the corner points of biggest contour
        # print(gradeContour) print the corner points of grade rectangle
        #print(biggestContour.shape)
        biggestContour=utilis.reorder(biggestContour)
        gradeContour=utilis.reorder(gradeContour)

        if biggestContour.size!=0 and gradeContour.size!=0:
            cv2.drawContours(imgContourBiggest,biggestContour,-1,(0,255,0),15)
            cv2.drawContours(imgContourBiggest,gradeContour,-1,(255,0,0),15)

        pt1=np.float32(biggestContour)
        pt2=np.float32([[0,0],[width,0],[0,height],[width,height]])
        matrix=cv2.getPerspectiveTransform(pt1,pt2)
        imgWarpColoured=cv2.warpPerspective(img,matrix,(width,height))

        ptg1=np.float32(gradeContour)
        ptg2=np.float32([[0,0],[280,0],[0,160],[280,160]])
        matrixG=cv2.getPerspectiveTransform(ptg1,ptg2)
        imgGradeDisplay=cv2.warpPerspective(img,matrixG,(280,160))
        #cv2.imshow("grade",imgGradeDisplay)

        #apply threshold
        imgWrapGrey=cv2.cvtColor(imgWarpColoured,cv2.COLOR_BGR2GRAY)
        imgThreshold= cv2.threshold(imgWrapGrey,200,255,cv2.THRESH_BINARY_INV)[1]

        ##################################################################################################
        boxes=utilis.splitBoxes(imgThreshold)
        #cv2.imshow("box",boxes[4])
        myPixelValues=np.zeros((questions,options))
        countC=0
        countR=0
        for i in boxes:
            totalPixels=cv2.countNonZero(i)
            myPixelValues[countR][countC]=totalPixels
            countC+=1
            if countC==options:
                countR+=1
                countC=0
        #print(myPixelValues)

        myIndex=[]
        for x in range(0,questions):
            arr=myPixelValues[x]
            #print("arr:",arr)
            myIndexVal=np.where(arr==np.amax(arr))
            #print(myIndexVal[0])
            myIndex.append(myIndexVal[0][0])
        #print(myIndex)

        #Grading##########################################################
        grading=[]
        for x in range(0,questions):
            if answers[x]==myIndex[x]:
                grading.append(1)
            else:
                grading.append(0)
        #print(grading)
        ################################score##########################################
        score=(sum(grading)/questions)*100
        print(score)

        #############################################################################
        imgAnswers = imgWarpColoured.copy()
        imgAnswers= imgAnswers[:, 100:img.shape[1] - 50]##crop from left and right
        imgAnswers = imgAnswers[30:img.shape[0] - 50, :]##crop the top
        imgAnswers=cv2.resize(imgAnswers,(width,height))
        imgAnswers=utilis.showAnswers(imgAnswers,myIndex,grading,answers,questions,options)
        ##########################################################################################################

        imgRawDrawing=np.zeros_like(imgWarpColoured)
        imgRawDrawing=utilis.showAnswers(imgRawDrawing,myIndex, grading, answers, questions, options)

        ############################################################################################################
        ###############restoring original image################################
        crop_top = 30
        crop_bottom = 50
        crop_left = 100
        crop_right = 50
        imgRawDrawing = cv2.copyMakeBorder(
            imgRawDrawing,
            crop_top,  # Top padding
            crop_bottom,  # Bottom padding
            crop_left,  # Left padding
            crop_right,  # Right padding
            cv2.BORDER_CONSTANT,# Border type
            value=[0, 0, 0]
        )
        imgRawDrawing=cv2.resize(imgRawDrawing,(width,height))
        invmatrix=cv2.getPerspectiveTransform(pt2,pt1)
        imgInverse=cv2.warpPerspective(imgRawDrawing,invmatrix,(width,height))
        imgFinal=img.copy()
        ##################################################################################################################

        imgRawGrade=np.zeros_like(imgGradeDisplay)
        cv2.putText(imgRawGrade,str(int(score))+"%",(60,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,110,0),3)
        #cv2.imshow("grade",imgRawGrade)
        InvMatrixG=cv2.getPerspectiveTransform(ptg2,ptg1)
        imgInvGrade=cv2.warpPerspective(imgRawGrade,InvMatrixG,(width,height))

        #cv2.imshow("efwe",imgInvGrade)

        imgFinal=cv2.addWeighted(imgFinal,1,imgInverse,1,0)
        #imgFinal=cv2.addWeighted(imgFinal,1,imgInvGrade,1,0)
        imgFinal = cv2.addWeighted(imgFinal, 0.7, imgInvGrade, 3, 0)
        cv2.imshow("final sheet",imgFinal)


        # print("imgInvGrade Shape:", imgInvGrade.shape)
        # print("imgFinal Shape:", imgFinal.shape)

        imgArray=[[img,imgGray,imgBlur,imgCanny,imgContours,imgContourBiggest],[imgWarpColoured,imgThreshold,imgAnswers,imgRawDrawing,imgInverse,imgFinal]]

    except:
        imgArray=[[img,imgGray,imgBlur,imgCanny,imgBlank,imgBlank],[imgBlank,imgBlank,imgBlank,imgBlank,imgBlank,imgBlank]]

    imgStack = stack.stackImages(0.4, imgArray)
    cv2.imshow("Image stack",imgStack)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("finalResult.jpg",imgFinal)
        cv2.waitKey(300)




