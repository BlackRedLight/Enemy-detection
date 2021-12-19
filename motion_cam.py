import time
import cv2
import sys


class MotionCamera:
	def __init__(self, sensitivity=25, minArea=5000):
		print('Initializing camera...')
		self.cap = cv2.VideoCapture(0)  # initialize webcam
		success, self.frame = self.cap.read()  # warmup camera and initailize first frame
		if success:
			print('Camera is working')
		else:
			self.cap.release()
			cv2.destroyAllWindows()
			print('Can\'t access the camera')
			sys.exit()
		self.sensitivity = sensitivity  # the bigger - the less motion
		self.minArea = minArea  # min area of motion contour


	def read_frame(self):
		_, self.frame = self.cap.read()
		return self.frame


	def find_motion(self, frame, lastFrame):
		frameDelta = cv2.absdiff(lastFrame, frame)
		thresh = cv2.threshold(frameDelta, self.sensitivity, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[0]	
		return cnts


	def convert_image(self, frame):
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
		return gray


	def refresh_bg(self, bgCount=3):
		self.bg = None
		bgI = 0
		lastFrame = None
		while True:
			success, self.frame = self.cap.read()

			gray = MotionCamera.convert_image(self, self.frame)

			if lastFrame is None:
				lastFrame = gray
				continue

			time.sleep(1.0)

			bgCnts = self.find_motion(gray, lastFrame)

			if bgCnts != ():
				lastFrame = gray
				bgI = 0
				print('Searching for background') 

			elif bgCnts == ():
				bgI += 1
				if bgI == bgCount:  # background found
					print('Background found')
					self.bg = gray
					break


	def motion_coordinates(self):
		gray = MotionCamera.convert_image(self, self.frame)
		cnts = MotionCamera.find_motion(self, gray, self.bg)

		i = 0
		boxes = []
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) >= self.minArea:
				# compute the bounding box for the contour and draw it on the frame
				(x, y, w, h) = cv2.boundingRect(c)
				boxes.append([x, y, x+w, x+h])
				i += 1
		return i,boxes


	def motion_frame(self):
		boxes = MotionCamera.motion_coordinates(self)
		markedFrame = self.frame
		print(boxes)
		for box in boxes[1]:
			if box != []:
				x, y, w, h = box
				cv2.rectangle(markedFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		return markedFrame


	def destroy(self):
		self.cap.release()
		cv2.destroyAllWindows()
		print('I through it on the ground')


if __name__ == '__main__':
	cam = MotionCamera()
	cam.refresh_bg()  # initialize a background

	while True:
		cam.read_frame()  # refresh frame in object
		boxes = cam.motion_coordinates()

		if boxes[0] == 0:  # number of boxes
			# save it sometimes at "neg" folder with txt file
			# and sometimes refresh background
			pass
		else:
			# save it at "pos" folder with txt file with coordinates
			# and save marked frame in another folder for understanding
			pass

		cv2.imshow('Motion frame', frame)
		if cv2.waitKey(100) == ord('q'):
			break

	cam.destroy()
	sys.exit()
