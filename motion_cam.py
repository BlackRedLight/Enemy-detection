import time
import cv2


cap = cv2.VideoCapture(0)
firstFrame = None
treshSensitivity = 15
min_area = 5000

# loop over the frames of the video
while True:
	# grab the current frame
	success, frame = cap.read()
	# let my webcam warmup and grab new frame
	if firstFrame is None:
		time.sleep(5.0)
		success, frame = cap.read()

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
	thresh = cv2.threshold(frameDelta, treshSensitivity, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[0]	
	
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) >= min_area:
			# compute the bounding box for the contour and draw it on the frame
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
	cv2.imshow("Motion camera", frame)
	if cv2.waitKey(250) == ord('q'):
		break
	
cap.release()
cv2.destroyAllWindows()