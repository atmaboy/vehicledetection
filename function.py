import cv2
import cv2.cv as cv
from datetime import datetime, time
import time
import logging
import numpy as np


def linedraw(frame,dim,status,savePoint):
    frm 	= cv.fromarray(frame)
    pointx 	= (0+20,savePoint)
    pointy 	= (dim[0]-20 , savePoint)
    if status == "danger":
    	cv.Line(frm, pointx, pointy, (255,0,0), 1)
    else:
    	cv.Line(frm, pointx, pointy, (255,255,255), 1)
    return

def linedrawCamera(frame,savePoint):
    frm     = cv.fromarray(frame)    
    cv.Line(frm, (20,savePoint), (220,savePoint), (255,0,0), 1)    
    return

def findcenter(x,y):	
	xcenter = x/2
	ycenter = y/2
	return xcenter,ycenter

def avgExecutionTime(totaldetect,totalelapsed):
	return float(totalelapsed / totaldetect)
