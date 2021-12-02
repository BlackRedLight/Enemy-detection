import cv2
import matplotlib


if __name__ == "__main__":
	test_img = './Enemy images/Pigeon.jpg'

	# img = cv2.imread(test_img)
	# cv2.imshow('Enemy', img)
	# cv2.waitKey(0)

	frameWidth = 640
	frameHeight = 480
	cap = cv2.VideoCapture(0)
	cap.set(3, frameWidth)
	cap.set(4, frameHeight)
	cap.set(10, 150)
	while True:
		success, img = cap.read()
		cv2.imshow("Result", img)
		cv2.waitKey(0)
		# break