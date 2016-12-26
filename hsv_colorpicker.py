#!/usr/bin/env python

import numpy as np
import time
import cv2 as cv

def searchWite(minc, maxc):

	def nothing(x):
		pass

	cap = cv.VideoCapture(0)
	cv.namedWindow("hsvTrack")
	cv.namedWindow("hsv")
	cv.namedWindow("mask")
	cv.moveWindow("hsvTrack", 0,0)
	cv.moveWindow("hsv", 800,600)
	cv.moveWindow("mask",400,0)

	cv.createTrackbar("Hmin", "hsvTrack", minc[0], 255, nothing)
	cv.createTrackbar("Hmax", "hsvTrack", maxc[0], 255, nothing)
	cv.createTrackbar("Smin", "hsvTrack", minc[1], 255, nothing)
	cv.createTrackbar("Smax", "hsvTrack", maxc[1], 255, nothing)
	cv.createTrackbar("Vmin", "hsvTrack", minc[2], 255, nothing)
	cv.createTrackbar("Vmax", "hsvTrack", maxc[2], 255, nothing)
	hmin = 0; hmax = 255; smin = 0; smax = 255; vmin = 0; vmax = 255

	try:
		while cap.isOpened():

			ret, frame = cap.read()
			if ret:

				hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

				mask = cv.inRange(hsv, (hmin, smin, vmin), (hmax, smax, vmax))
				mask = cv.erode(mask, None, iterations=2)
				mask = cv.dilate(mask, None, iterations=2)

				cv.imshow("mask", mask)
				cv.imshow("hsv", hsv)

				hmin = cv.getTrackbarPos("Hmin", "hsvTrack")
				hmax = cv.getTrackbarPos("Hmax", "hsvTrack")
				smin = cv.getTrackbarPos("Smin", "hsvTrack")
				smax = cv.getTrackbarPos("Smax", "hsvTrack")
				vmin = cv.getTrackbarPos("Vmin", "hsvTrack")
				vmax = cv.getTrackbarPos("Vmax", "hsvTrack")
					
				if cv.waitKey(1) & 0xFF == ord('q'):
					print("End")
					cap.release()
					cv.destroyAllWindows()
					return True
			else:
				return True
	except KeyboardInterrupt:
		print("END with except")
		cap.release()
		cv.destroyAllWindows()
		return False

minc = [0,0,0]
maxc = [255,255,255]

while searchWite(minc, maxc):
	pass