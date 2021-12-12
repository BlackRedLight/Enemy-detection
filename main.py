import cv2
import matplotlib


if __name__ == "__main__":
	
	frameWidth = 640
	frameHeight = 480
	cap = cv2.VideoCapture(0)
	# cap.set(3, frameWidth)
	# cap.set(4, frameHeight)
	#cap.set(10, 150)  # brightness

	while True:
		success, img = cap.read()
		
		if not success:
			print("Can't receive frame (stream end?). Exiting ...")
			break

		cv2.imshow("Result", img)
		
		if cv2.waitKey(1) == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()