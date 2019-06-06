import cv2 
import numpy as np 
import time

# Class to find the foreign matters in the highway. 
class FMFinding():

	def __init__(self, width = 960, height = 540, accu_number = 30000, fm_threshold = 50):
		self.frame_index = 0
		self.w = width
		self.h = height
		self.accu_number = 30000 # 25 frames per second, default 20 minutes. 
		self.fm_threshold = 50 # threshold of the foreign matters that diff with the background. 	

		#self.curr_frame = None
		self.acum_frame = None
		self.acum_contours = None
		self.acum_contours_base = None



	def init_acum_frame(self):
		self.acum_frame = np.zeros(shape = (self.h, self.w), dtype = np.uint32)

	def init_acum_contours(self):
		self.acum_contours = np.zeros(shape = (self.h, self.w), dtype = np.int16)

	def add_new_frame(self, new_frame):
		frame = cv2.resize(new_frame, (self.w, self.h), interpolation = cv2.INTER_LINEAR)
		#self.curr_frame = frame
		self.frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		
		if self.acum_frame is None:
			self.init_acum_frame()

		self.acum_frame += self.frame_gray
		self.frame_index += 1

		self.frame_avg = np.array((self.acum_frame // self.frame_index), dtype = np.uint8)

		if self.frame_index >= self.accu_number:
			self.acum_frame = self.acum_frame // 2
			self.frame_index = self.frame_index // 2

	def phase_frame(self, new_frame):
		#self.addNewFrame(new_frame)
		frame = cv2.resize(new_frame, (self.w, self.h), interpolation = cv2.INTER_LINEAR)
		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		frame_delta = cv2.absdiff(self.frame_avg, frame)

		thresh = cv2.threshold(frame_delta, self.fm_threshold, 255, cv2.THRESH_BINARY)[1]
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

		return max_contours

	def get_frame_index(self):
		return self.frame_index

	# Return the accumulate frame which has no moving objects. 
	def get_standard_frame(self):
		return self.frame_avg

	# Return the previous frame that added. (already transfer to gray.) 
	def get_gray_frame(self):
		return self.frame_gray

	# Return a frame that mark the contours in current input frame. 
	def get_contours_frame(self):
		_, frame = cv2.threshold(self.acum_contours, 248, 248, cv2.THRESH_TRUNC)
		frame = np.array(frame, dtype = np.uint8)
		return frame 
















