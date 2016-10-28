#  _______________________________________________________________________________
# | car detection and distance measurement using haar cascade and opencv library  |
# | created by      = Atmaji Haryo Wiryawan                                       |
# | time developed  = start on June 2016                                          |
# | code type       = open frame                                                 |
# |                                                                               |
# | use this code for reference or learning purpose only, please do not use this  |
# | code for commercial private , group or company benefit.                       |
# |_______________________________________________________________________________|


import cv2
import cv2.cv as cv
from datetime import datetime, time
import time
import logging
import numpy as np

import function
import bitmapto8bit


cap                     = cv2.VideoCapture('tes1.mp4')
fps 				    = cap.get(cv2.cv.CV_CAP_PROP_FPS)
#fps                     = "null"

font                    = cv2.FONT_HERSHEY_SIMPLEX
report                  = open('report.txt','w+r')
time_execution_start    = str(datetime.now()) + "\n"
classifier              = cv2.CascadeClassifier('Classifier/cars_new.xml')
point                   = input("enter save point 50-80 : ")
ncars                   = 0
y                       = 0
nfalse                  = 0
totaldetect             = 0
totalelapsed            = 0


while True :
    start_time  = time.time()
    ret, image  = cap.read()        
    r           = 320.0 / image.shape[1]
    dim         = (320, int(image.shape[0] * r))
    savePoint   = dim[1]*point/100
    
    imgs        = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) #resize image
    frame       = cv2.cvtColor(imgs, cv2.COLOR_RGB2GRAY)
    #frame      = bitmapto8bit.main(frames)
    vehicles    = classifier.detectMultiScale(frame, 
                                       1.1,
                                       1,
                                       cv2.cv.CV_HAAR_SCALE_IMAGE)
    frm         = cv.fromarray(frame)

    for (x,y,w,h) in vehicles:        
        crop_imgs   = frame[y:(y+h), x:(x+w)] # Crop from x, y, w, h -> 100, 200, 300, 400            
        xcentre,ycentre    = function.findcenter(x,y)        
        if x+w >= 80 & x+w <= 150:
            rect        = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),2)
            # ncars = 0
            if (y+h) >= savePoint:
                function.linedraw(frame,dim,"danger",savePoint)
                cv2.putText(frame,'tidak aman',(x,y-3),font,0.3,(0,0,255))
                print ("tidak aman")
            elif (y+h) < savePoint:
                function.linedraw(frame,dim,"save",savePoint)
                cv2.putText(frame,'aman',(x,y-3),font,0.3,(0,255,0))                
                print ("aman")                        
            ncars       = ncars + 1
            y           = y + 1
            i           = str(ncars)
            cv2.putText(frame,i,(150,20),font,0.5,(0,0,0))            
            totaldetect = totaldetect + y
            end_time        = time.time()
            elapsed_time    = float(end_time - start_time)
            totalelapsed    = totalelapsed + elapsed_time
            print "waktu eksekusi %f" % (elapsed_time)
        elif x+w < 80 & x+w > 150:
            nfalse      = nfalse + 1
            # totaldetect = totaldetect + nfalse
    
    cv2.putText(frame,'mobil terdeteksi: ',(10,20),font,0.5,(0,0,0))
    ncars       = 0
    # cv2.putText(frame,'fps : ' + str(fps),(160,110),font,0.3,(0,0,0))
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):            
        avgExec             = function.avgExecutionTime(y,totalelapsed)
        report_totaldetect  = "total detect : " + str(totaldetect) + "\n"
        report_totalfalse   = "total false detect : " + str(nfalse) + "\n"            
        report_averageexec  = "average execution time : " + str(avgExec) + "\n"
        time_execution_stop = str(datetime.now()) + "\n"

        report.write(time_execution_start)      
        report.write(report_totaldetect)
        report.write(report_totalfalse)
        report.write(report_averageexec)
        report.write(time_execution_stop)
        report.close()
        break

cv2.waitKey()
cv2.destroyAllWindows()

# def linedraw(frame):
# frm = cv.fromarray(frame)
# cv.Line(frm, (0,dim[1]/1.5), (dim[0],dim[1]/1.5), (255,255,255), 1)
# return

