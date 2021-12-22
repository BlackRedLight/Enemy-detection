import motion_cam
import cv2
import sys


if __name__ == '__main__':
	cam = motion_cam.MotionCamera()
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

		cv2.imshow('Motion frame', cam.motion_frame())
		if cv2.waitKey(100) == ord('q'):
			break

	cam.destroy()
	sys.exit()