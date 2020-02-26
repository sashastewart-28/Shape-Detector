from __future__ import print_function
import cv2
import numpy as np
import imutils
import time


scale = 2
cap = cv2.VideoCapture(0)
print ("press q to quit")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))

while(cap.isOpened()):
    ret,frame = cap.read()
    resized = imutils.resize(frame, width=300)
    ratio = frame.shape[0] / float(resized.shape[0])
    if ret == True:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)[1]
        sigma = 1.5
        v = np.median(gray)
        low = int(max(0,(1.0+sigma)*v))
        high = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(gray,low,high,1)
        contours = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        contours
        contours = contours[0] if imutils.is_cv2() else contours[1]

        for c in contours:
            M = cv2.moments(c)
            try:
                cX = int((M["m10"]/M["m00"])*ratio)
            except:
                continue
            cY = int((M["m01"]/M["m00"])*ratio)
            cv2.drawContours(frame,[c],-1,(0,255,0),2)
            peri = cv2.arcLength(c,True)
            vertices = cv2.approxPolyDP(c,cv2.arcLength(c,True)*0.02,True)

            if (len(vertices) == 3):
                cv2.putText(frame,'TRIANGLE',(cX,cY),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)

            elif (len(vertices) == 4):
                x, y, w, h = cv2.boundingRect(vertices)
                aspectratio = float(w)/h
                if aspectratio>=0.95 and aspectratio<=1.05:
                    cv2.putText(frame, 'SQUARE', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                else:
                    cv2.putText(frame, 'RECTANGLE', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            elif (len(vertices) > 5 and len(vertices) < 20):
                cv2.putText(frame, 'STAR', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            else:
                cv2.putText(frame, 'CIRCLE', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        out.write(frame)
        cv2.imshow('frame',frame)
        cv2.imshow('canny',edged)
        if cv2.waitKey(1) == 1048689:
            break


cap.release()
cv2.destroyAllWindows()