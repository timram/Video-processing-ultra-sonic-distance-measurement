"""
This module allow you to test values of hsv that you 
have found if hsv_colopicker module.

Just add this values to color variable of ColorSelect class
in form like: "color_name": ((hmin, smin, vmin), (hmax, smax, vmax), (r, g, b))
"""

import numpy as np 
import cv2 as cv

class ColorSelect(object):

	def __init__(self):
		self.color = {"blue":((92,133,0),(140,255,255),(255,0,0)), "red":((161,137,140),(188,250,231),(0,0,255)),
		"skin":((100,47,83),(204,128,255),(0,255,0)), "light":((0,0,169),(82,8,255),(0,255,0)), 
		"green":((35,36,122),(82,117,255),(0,255,0))}

	def SelectColor(self,frame, mask, color):
		cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)[-2]
		center = None

		if len(cnts) > 0:
			c = max(cnts, key=cv.contourArea)
			((x, y), radius) = cv.minEnclosingCircle(c)
			M = cv.moments(c)
			if M["m00"] != 0:
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			if radius > 10:
				cv.circle(frame, (int(x), int(y)), int(radius), color, 2)
				cv.circle(frame, center, 5, (0,0,255),-1)

	def filterAndSelctColor(self, frame, lookColor):
		hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
		masks = [cv.inRange(hsv, self.color[key][0], self.color[key][1]) for key in self.color if key in lookColor]
		colors = [self.color[key][2] for key in self.color if key in lookColor]
		for i in range(len(masks)):
			masks[i] = cv.erode(masks[i], None, iterations=2)

		for i in range(len(masks)):
			masks[i] = cv.dilate(masks[i], None, iterations=2)
			print(masks[i])

		for i in range(len(masks)):
			self.SelectColor(frame, masks[i], colors[i])

cv.namedWindow("frame")

cap = cv.VideoCapture(0)

clrslct = ColorSelect()
colors = raw_input("Enter colors that you want to select(blue, red, green, skin, light)\n")
colors = colors.split(' ')

while cap.isOpened():

	ret,frame = cap.read()

	clrslct.filterAndSelctColor(frame,colors)

	cv.imshow("frame", frame)

	if cv.waitKey(1) & 0xFF == ord('q'):
		print("End")
		break

cap.release()
cv.destroyAllWindows()
