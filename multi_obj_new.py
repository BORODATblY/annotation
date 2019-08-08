#python multi_obj.py --tracker csrt
#sudo pip install opencv-contrib-python


# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import numpy as np

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())

# initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations
OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}

# initialize OpenCV's special multi-object tracker
trackers = cv2.MultiTracker_create()

# function called by trackbar, sets the next frame to be read
def getFrame(frame_nr):
    vs.set(cv2.CAP_PROP_POS_FRAMES, frame_nr)

#  function called by trackbar, sets the speed of playback
def setSpeed(val):
    global playSpeed
    playSpeed = max(val, 5)

def setFPS(val):
	global FPS
	FPS = max(val, 1)

# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)


	
	#otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])

image_name = str(args["video"])

folder_name = image_name[:-4]
try:
    if not os.path.exists(folder_name): 
    	# os.path.exists('save'):
    	# strftime("%Y%m%d", gmtime()) add data to name folder
        os.makedirs(folder_name) 
        # os.makedirs('save') 
        # strftime("%Y%m%d", gmtime()) create same + date folder
except OSError:
    print ('Error: Creating directory of save')


# loop over frames from the video stream
image_num = 0
# get total number of frames
nr_of_frames = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
# set wait for each frame, determines playbackspeed
playSpeed = 16

# get write FPS
FPS = 5


# add trackbar
cv2.namedWindow("Frame")
# create Trackbar rewinding
cv2.createTrackbar("Frames", "Frame", 0, nr_of_frames, getFrame)
# create Trackbar speed
cv2.createTrackbar("Speed", "Frame", playSpeed ,500, setSpeed)
# create Trackbar speed writing images
cv2.createTrackbar("Write FPS", "Frame", FPS, 30, setFPS)

while True:
	try:

		# grab the current frame, then handle if we are using a
		# VideoStream or VideoCapture object
		frame = vs.read()
		frame = frame[1] if args.get("video", False) else frame
		
		# check to see if we have reached the end of the stream
		if frame is None:
			break

		# resize the frame (so we can process it faster)
		frame = imutils.resize(frame, width = 1400)

		# grab the updated bounding box coordinates (if any) for each
		# object that is being tracked
		(success, boxes) = trackers.update(frame)
		
		# loop over the bounding boxes and draw then on the frame
		for box in boxes:
			(x, y, w, h) = [int(v) for v in box]

			if(h>w):
				crop_img = frame[y : y +h , x : x + h ]#+ w]
			if(w>h):
				crop_img = frame[y : y +w , x : x + w ]#+ w]

			#cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH),(0, 255, 0), 1)
			cv2.imshow("faces",crop_img)

			if(image_num % FPS):
				some=1
				# print("")
			else:
				# name image 
				# if you have old name:
				# cv2.imwrite("./save/hand" + str(image_num) + ".jpg", crop_img)
				
				cv2.imwrite("./"+ folder_name + "/" + image_name[:-4] + "_" + str(image_num) + ".jpg", crop_img)
			
			image_num+=1

			cv2.rectangle(frame, (x-1, y-1), (x + w +2, y + h +2), (0, 255, 0), 1)
		
			# show the output frame
		cv2.imshow("Frame", frame)
		# pos in life frame
		pos = vs.get(cv2.CAP_PROP_POS_FRAMES)
		
		cv2.setTrackbarPos("Frame","Frame", int(pos))
		
		key = cv2.waitKey(playSpeed) & 0xFF #5

		# if the 's' key is selected, we are going to "select" a bounding
		# box to track
		if key == ord("s"):
			# select the bounding box of the object we want to track (make
			# sure you press ENTER or SPACE after selecting the ROI)
			box = cv2.selectROI("Frame", frame, fromCenter=False,
				showCrosshair=True)

			# create a new object tracker for the bounding box and add it
			# to our multi-object tracker
			tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
			trackers.add(tracker, frame, box)

		if key == ord("c"):
			trackers = cv2.MultiTracker_create()
		
		# if the `q` key was pressed, break from the loop
		elif key == ord("q"):
			break
	except:
		print("err")

# if we are using a webcam, release the pointer
if not args.get("video", False):
	vs.stop()

# otherwise, release the file pointer
else:
	vs.release()

# close all windows
cv2.destroyAllWindows()
