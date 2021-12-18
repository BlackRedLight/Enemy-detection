import time
import cv2
import sys


class MotionCamera:
	def __init__(self):
		print('Initializing camera...')
		self.cap = cv2.VideoCapture(0)  # initialize webcam
		success, _ = self.cap.read()  # warmup camera
		if success:
			print('Camera is working')
		else:
			self.cap.release()
			cv2.destroyAllWindows()
			print('Can\'t access the camera')
			sys.exit()

	def refresh_bg(self):
		bg = None
		bgFound = False
		bgI = 0
		while True:
			success, frame = self.cap.read()
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (21, 21), 0)

			if lastFrame is None:
				lastFrame = gray
				continue


	def find_motion(self, frame, lastFrame):
		frameDelta = cv2.absdiff(lastFrame, frame)
		thresh = cv2.threshold(frameDelta, threshSensitivity, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[0]	
		return cnts

	def destroy(self):
		self.cap.release()
		cv2.destroyAllWindows()
		print('I through it on the ground')

cam = MotionCamera()
cam.destroy()
sys.exit()

cap = cv2.VideoCapture(0)
firstFrame = None
i = 0
background_found = False
threshSensitivity = 25
min_area = 5000

# loop over the frames of the video
while True:
	# grab the current frame
	success, frame = cap.read()

	if background_found is False:
		time.sleep(1.0)

	if not success:
		print('Can\'t read frames from the camera')
		break
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	
	# initialize background frame
	if firstFrame is None:
		firstFrame = gray
		continue
	
	# find new regions and draw contors
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, threshSensitivity, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[0]	
	
	

	if (cnts == ()) and (background_found is False) and (i < 3):
		i += 1
		if i == 3:
			background_found = True
		print('Background found')
		continue
	elif (cnts != ()) and (background_found is False):
		firstFrame = gray
		i = 0
		print('Working on it')
		continue


	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) >= min_area:
			# compute the bounding box for the contour and draw it on the frame
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	
	# cv2.imshow('Motion camera', frame)
	# cv2.imshow('FUCK', thresh)
	# cv2.imshow('Background', firstFrame)
	cv2.imshow('Motion', frame)
	if cv2.waitKey(25) == ord('q'):
		break
	
cap.release()
cv2.destroyAllWindows()