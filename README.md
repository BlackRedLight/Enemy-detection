# Description
Neural network, that detects pigeons and makes them get the hell out from me. This project based on OpenCV and uses Cascade Classifier. This project was built for learning purposes only. No pigeons was hurt in this project.

# Packages
All needed packages are listed in requirement.txt. To install packages enter `pip install -r requirement.txt` in your virtual environment.

# Instructions
1. Open terminal at project folder.
2. To run the program enter `python3 src/main.py`.
3. To run tests enter `python3 tests.py`, but they are not ready yet.

# Modules
## Motion camera
File: motionCam.py

Classes:
* MotionCamera(sensitivity, min_area)

Methods:
* MotionCamera.readFrame() - refreshes frame in object and returns the frame
* MotionCamera.refreshBg(bg_count) - sets a background to find movement
* MotionCamera.motionCoordinates() - returns number of boxes and their coordinates
* MotionCamera.motionFrame() - returns marked frame
* MotionCamera.destroy() - deletes a OpenCV object and closes it's windows

Variables:
* MotionCamera.frame - clean frame from webcam
* MotionCamera.sensitivity - how sensetive is the camera
* MotionCamera.min_area - minimum size of captured motions
* MotionCamera.bg - background frame
* MotionCamera.thresh - frame of what motion camera sees

Helps to find movements and can return both frames with marked boxes and list with number of boxes and their coordinates.

### MotionCamera()
To create a motion camera object use `motionCam.MotionCamera()`. It has two arguments: `sensitivity` and `min_area`.
* `senitivity` defines how it will be sensitive to differences between background frame and current frame. It can be an integer from 0 to 254. It is 25 by default. The bigger the number - the less movement it sees. You can see the difference by using `thresh` variable, which contains highlighted areas that camera sees.
* `min_area` defines how big movement areas must be so `motionCoordinates()` and `motionFrame()` will return them. The bigger the number - the bigger must be areas. It's 5000 by default.

```Python
import motion_cam as mc

cam = mc.MotionCamera(20, 4000)
cam.refresh_bg()
```
Ones it initialized it will automaticly turn on a camera and "warm up" it by reading first frame from it. It allowes camera to have some time to set it's brightness. If all this was successful it will print "Camera is working" message. If it failes to read a frame it will delete an OpenCV object and raise RuntimeError "Can't access the camera".


### MotionCamera.readFrame()
Reads a frame from the connected camera. Refreshes it in the object, so it can be used to find movements on it. It also returns this frame. Use it before `motionCoordinates()` and `motionFrame()`.

### MotionCamera.refreshBg(bg_count)
Sets a background. It will be base frame to find movements. Ones it's called it starts to search for background. It will look for `bg_count` frames in a row, that has no difference between one another. It uses `senitivity` setting. If your camera has a hard time to find a background try to raise up your `senitivity` setting.

### MotionCamera.motionCoordinates()
Find motion using `frame` and `bg` and return a tuple with number of boxes and a list of lists of coordinates of each movement box in format `(number, [[x1, y1, x2, y2],...])`.

Example:
`(2, [[0, 0, 36, 45], [25, 35, 125, 221]])`

### MotionCamera.motionFrame()
Make a green boxes around movements on a `frame`. It returns an OpenCV frame with boxes and do not changes the ofiginal `frame`.

### MotionCamera.destroy()
Destroies a camera object and closes all the OpenCV windows.