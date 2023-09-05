import cv2, imutils
import numpy as np

class Trackbar:

	img = None
	original = None
	dimensions = None
	center = None

	def access_properties(self, frame):
		self.img = frame
		temp = frame
		self.original = temp
		self.dimensions = self.img.shape

	# Displaying the coordinate system on the screen

	def click_event(self, event, x, y, flags, params):
		if event == cv2.EVENT_LBUTTONDOWN:
			self.center = (x,y)
			cv2.circle(self.img, (x,y), radius = 2, color = (0, 0, 255), thickness = 3)
			cv2.line(self.img, (0, y), (self.dimensions[1], y), (0, 0, 255), (2))
			cv2.line(self.img, (x, 0), (x, self.dimensions[0]), (0, 0, 255), (2))

	def coord_system(self):
		while(1):
			cv2.imshow('frame', self.original)
			cv2.setMouseCallback('frame', self.click_event)

			key = cv2.waitKey(1) & 0xFF 
			if key == ord('q'):
				break
		
		cv2.destroyAllWindows()

	def get_origin(self):
		return self.center	


