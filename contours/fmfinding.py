import cv2 
import numpy as np 
import time

# Class to find the foreign matter in the highway. 
class FMFinding():

	def __init__(self, width = 960, height = 540):
		self.frame_index = 0
		self.w = width
		self.h = height

		self.curr_frame = None
		self.acum_frame = None
		self.acum_contours = None
		self.acum_contours_base = None

		self.ACCUM_NUMBER = 100

	def init_acum_frame(self):
		self.acum_frame = np.zeros(shpae = (self.h, self.w), dtype = np.uint32)

	def init_acum_contours(self):
		self.acum_contours = np.zeros(shape = (self.h, self.w), dtype = np.int16)

	def addNewFrame(self, new_frame):
		frame = cv2.resize(new_frame, (self.w, self.h), interpolation = cv2.INTER_LINEAR)
		self.curr_frame = frame

		frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		self.frame_gray = frame_gray

		if self.acum_frame is None:
			self.init_acum_frame()

		self.acum_frame += image_gray
		self.frame_index += 1

		self.frame_avg = self.acum_frame // self.frame_index

		if frame_index >= 30000:
			acum_frame = acum_frame // 2
			frame_index = frame_index // 2

	def phaseFrame(self, new_frame):
		self.addNewFrame(new_frame)

		frame_delta = cv2.absdiff(self.frame_avg, self.frame_gray)

		thresh = cv2.threshold(frame_delta, 50, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations = 2)

		if cv2.__version__[0] == '3':
			_, contours, hierarchy = cv2.findContours(thresh.copy(), 
													  cv2.RETR_EXTERNAL, 
													  cv2.CHAIN_APPROX_SIMPLE)
		else:
			contours, hierarchy = cv2.findContours(thresh.copy(), 
												   cv2.RETR_EXTERNAL, 
												   cv2.CHAIN_APPROX_SIMPLE)

		contours_valid = []
		for item in contours:
			area = cv2.contourArea(item)
			if area > 300 and area < 50000:
				contours_valid.append(item)	

		frame_contours = cv2.drawContours(np.zeros(shape = (self.h, self.w), dtype = np.int8), 
										  contours_valid, -1, 2, -1)

		if self.acum_contours is None:
			self.init_acum_contours()

		self.acum_contours += frame_contours
		self.acum_contours -= 1

		_, self.acum_contours = cv2.threshold(self.acum_contours, 0, 65535, cv2.THRESH_TOZERO)

		max_contours = self.acum_contours.max()








