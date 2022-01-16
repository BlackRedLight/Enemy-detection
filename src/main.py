import motionCam as mc
import cv2
import sys
import os


if __name__ == '__main__':
	cam = mc.MotionCamera()  # Initialize a motion camera
	cam.refreshBg()  # Initialize a background

	calm = 0  # Number of static frmaes  in a row
	
	while True:
		cam.readFrame()  # Refresh frame in object
		boxes = cam.motionCoordinates()  # Get number of boxes and their coordinates

		if boxes[0] == 0:  # number of boxes
			''' save it sometimes at "neg" folder with txt file
			and sometimes refresh background '''
			
		else:
			# save it at "pos" folder with txt file with coordinates
			# and save marked frame in another folder for understanding
			pass

		cv2.imshow('Motion frame', cam.motionFrame())
		if cv2.waitKey(100) == ord('q'):
			break

	cam.destroy()
	sys.exit()