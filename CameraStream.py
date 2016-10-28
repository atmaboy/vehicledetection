from picamera.array import PiRGBArray
from picamera import PiCamera

from datetime import datetime, time
import time
import logging
import numpy as np

import cv2
import cv2.cv as cv

import bitmapto8bit
import function

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 20
rawCapture = PiRGBArray(camera, size=(320,240))
time.sleep(0.1)

classifier              = cv2.CascadeClassifier('classifier.xml')


font                    = cv2.FONT_HERSHEY_SIMPLEX
report                  = open('report_camera.txt','w')
time_execution_start    = str(datetime.now()) + "\n"
point                   = input("enter save point 50-80 : ")
ncars                   = 0
nfalse                  = 0
totaldetect             = 0
totalelapsed            = 0
savePoint               = point

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    start_time  = time.time()
    
    image       = frame.array
    frames      = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)    
    convFrame   = bitmapto8bit.main(frames)
    vehicles    = classifier.detectMultiScale(convFrame, 
                                           1.1,
                                           1,
                                           cv2.cv.CV_HAAR_SCALE_IMAGE
                                           )
    for (x,y,w,h) in vehicles:
        xcentre,ycentre    = function.findcenter(x,y) 
        if x+w >= 80 & x+w <= 110:
            rect        = cv2.rectangle(convFrame,(x,y),(x+w,y+h),(0,0,0),2)                
            totaldetect = totaldetect + ncars
            i           = str(ncars)                
            cv2.putText(convFrame,i,(150,20),font,0.5,(0,0,0))
            if (y+h) >= savePoint:                
                function.linedrawCamera(convFrame,savePoint)
                cv2.putText(convFrame,'tidak aman',(x,y-3),font,0.3,(0,0,255))
                ncars       = ncars + 1
                print ("tidak aman")
            elif (y+h) < savePoint:
                function.linedrawCamera(convFrame,savePoint)
                cv2.putText(convFrame,'aman',(x,y-3),font,0.3,(0,255,0))
                ncars       = ncars + 1
                print ("aman")
            ncars       = ncars + 1
            totaldetect = totaldetect + ncars
            end_time        = time.time()
            elapsed_time    = float(end_time - start_time)
            totalelapsed    = totalelapsed + elapsed_time
            print "waktu eksekusi %f" % (elapsed_time)
        elif x+w < 80 & x+w > 150:
            nfalse      = nfalse + 1
            # totaldetect = totaldetect + nfalse        
    
    cv2.putText(convFrame,'mobil terdeteksi: ',(10,20),font,0.5,(0,0,0))    
    cv2.imshow("frame", convFrame)
    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        avgExec             = function.avgExecutionTime(totaldetect,totalelapsed)
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

    
    
