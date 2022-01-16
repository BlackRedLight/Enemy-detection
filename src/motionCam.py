import time
import cv2
import sys


class MotionCamera:
	def __init__(self, sensitivity=25, min_area=5000):
		''' Warm up the camera. Raises RuntimeError if it'll fail.
		sensitivity - the bigger - the less motion will be captured
		min_area - minimum size of movement areas for boxes'''
		
		print('Initializing a camera...')
		self.cap = cv2.VideoCapture(0)  # initialize webcam
		success, self.frame = self.cap.read()  # warmup camera and initailize first frame
		if success:
			print('Camera is working')
		else:
			self.cap.release()
			cv2.destroyAllWindows()
			return RuntimeError('Can\'t access the camera')
			sys.exit()
		self.sensitivity = sensitivity  # the bigger - the less motion captured
		self.min_area = min_area  # min area of motion contour


	def readFrame(self):
		''' Reads a frame from a camera and refreshes it in the object '''
		
		_, self.frame = self.cap.read()
		return self.frame


	def __findMotion(self, frame, last_frame):
		''' Finds contours of a motions. Returns an OpenCV contour '''
		
		frame_delta = cv2.absdiff(last_frame, frame)
		self.thresh = cv2.threshold(frame_delta, self.sensitivity, 255, 
			cv2.THRESH_BINARY)[1]
		self.thresh = cv2.dilate(self.thresh, None, iterations=2)
		cnts = cv2.findContours(self.thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[0]	
		return cnts


	def __convertImage(self, frame):
		''' Converts a frame into blured gray frame 
		frame - clean frame to convert'''
		
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
		return gray


	def refreshBg(self, bg_count=5):
		''' Creates a background frame to compare
		further frames and find movements.
		bg_count - how much static frames in a row to search'''
		
		self.bg = None
		bg_i = 0
		last_frame = None
		while True:
			success, self.frame = self.cap.read()

			gray = MotionCamera.__convertImage(self, self.frame)

			if last_frame is None:
				last_frame = gray
				continue

			time.sleep(1.0)

			bg_cnts = self.__findMotion(gray, last_frame)

			if bg_cnts != ():
				last_frame = gray
				bg_i = 0
				print('Searching for background') 

			elif bg_cnts == ():
				bg_i += 1
				if bg_i == bg_count:  # background found
					print('Background found')
					self.bg = gray
					break


	def motionCoordinates(self):
		''' Find motion and return a tuple with number of boxes and a list
		of coordinates of each movement box.
		(number, [[x1, y1, x2, y2], [x1, y1, x2, y2]...])'''
		
		gray = MotionCamera.__convertImage(self, self.frame)
		cnts = MotionCamera.__findMotion(self, gray, self.bg)

		i = 0
		boxes = []
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) >= self.min_area:
				# compute the bounding box for the contour and draw it on the frame
				x, y, w, h = cv2.boundingRect(c)
				boxes.append([x, y, x+w, y+h])
				i += 1
		return i, boxes


	def motionFrame(self):
		''' Make a frame with boxes around movements on it '''
		
		boxes = MotionCamera.motionCoordinates(self)
		marked_frame = self.frame
		for box in boxes[1]:
			if box != []:
				x1, y1, x2, y2 = box
				cv2.rectangle(marked_frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
		return marked_frame


	def destroy(self):
		''' Destroy a camera object '''
		
		self.cap.release()
		cv2.destroyAllWindows()
		print('I through it on the ground')


if __name__ == '__main__':
	cam = MotionCamera()
	cam.refreshBg()  # initialize a background

	while True:
		cam.readFrame()  # refresh frame in object
		boxes = cam.motionCoordinates()
		print(boxes)
		
		frame = cam.motionFrame()
		cv2.imshow('Motion frame', frame)
		cv2.imshow('Threshhold', cam.thresh)
		if cv2.waitKey(200) == ord('q'):
			break

	cam.destroy()
	sys.exit()
