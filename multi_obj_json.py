# How to install
# sudo apt install python-opencv
# sudo pip install opencv-contrib-python
# How to run
# python3 multi_obj_json.py --tracker csrt  --video "05 feet MG Weapon Away From Body.MP4"
# How to use
# Put "s" button to show region with mouse
# Put "c" to stop cropping this region
# Put "q" to quit

# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
from pathlib import Path
import numpy as np
import pafy
import re

import json



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

def setFPS(val):
	global FPS
	FPS = max(val, 1)

def getFrame(frame_nr):
    #frame_nr = video.length
    vs.set(cv2.CAP_PROP_POS_FRAMES, frame_nr)
#  function called by trackbar, sets the speed of playback

def setSpeed(val):
    global playSpeed
    playSpeed = max(val, 5)

try:
	url = args["video"]
	video = pafy.new(url)
	play = video.getbest(preftype = "mp4")
	vs = cv2.VideoCapture(play.url)
	image_name = str(video.title)
	image_name = image_name.replace("/", " ")
	
	folder_name = str(video.title)
	folder_name = folder_name.replace("/", " ")
	filename = str(folder_name)
	download = 1
# if a video path was not supplied, grab the reference to the web cam
except:
	if not args.get("video", False):
		print("[INFO] starting video stream...")
		vs = VideoStream(src=0).start()
		time.sleep(1.0)
	#otherwise, grab a reference to the video file
	else:
		vs = cv2.VideoCapture(args["video"])

	image = str(args["video"])
	image_name = image [:-4]
	folder_name = image_name
	download = 0

try:
    if not os.path.exists(folder_name): 
    	# os.path.exists('save'):
    	# strftime("%Y%m%d", gmtime()) add data to name folder
        os.makedirs(folder_name) 
        # create folder up, down, left, right
        #os.makedirs("./" + folder_name + "/" + "screenshots")
        
        #os.makedirs("./" + folder_name + "/" + "screenshots")
        # strftime("%Y%m%d", gmtime()) create save + date folder
except OSError:
    print ('Error: Creating directory of save')

nr_of_frames = int(vs.get(cv2.CAP_PROP_FRAME_COUNT)) 

# loop over frames from the video stream
image_num=0

playSpeed = 16

# get write FPS
FPS = 60

# add trackbar
cv2.namedWindow("Frame")
# create Trackbar rewinding
cv2.createTrackbar("Frames", "Frame", 0, nr_of_frames, getFrame)
# create Trackbar speed
cv2.createTrackbar("Speed", "Frame", playSpeed ,500, setSpeed)
# create Trackbar speed writing images
cv2.createTrackbar("Write FPS", "Frame", FPS, 50, setFPS)



#data = {}
#data['_via_img_metadata'] = []

#f = open("./folder_name/data.json","w+")
#settings = ' {"_via_settings":{"ui":{"annotation_editor_height":25,"annotation_editor_fontsize":0.8,"leftsidebar_width":18,"image_grid":{"img_height":80,"rshape_fill":"none","rshape_fill_opacity":0.3,"rshape_stroke":"yellow","rshape_stroke_width":2,"show_region_shape":true,"show_image_policy":"all"},"image":{"region_label":"__via_region_id__","region_color":"__via_default_region_color__","region_label_font":"10px Sans","on_image_annotation_editor_placement":"NEAR_REGION"}},"core":{"buffer_size":"18","filepath":{},"default_filepath":""},"project":{"name":"via_project_28Aug2019_23h45m"}}'
#f.write(settings)

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
		
		#frame = imutils.resize(frame, width = 1300)
		# grab the updated bounding box coordinates (if any) for each
		# object that is being tracked
		(success, boxes) = trackers.update(frame)

		# loop over the bounding boxes and draw then on the frame
		for box in boxes:
			(x, y, w, h) = [int(v) for v in box]

			height, width, channels = frame.shape 
			if(x + w +2> width or y + h +2>height):
				break

			if(h>w):
				crop_img = frame[y : y +h , x : x + h ]#+ w]
			if(w>h):
				crop_img = frame[y : y +w , x : x + w ]#+ w]

			#cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH),(0, 255, 0), 1)
			#cv2.imshow("faces",crop_img)



# Save folder and name 
# you can chenge this 
			
			
			#cv2.imwrite("./save/" + name , frame)    # cropped 
			#cv2.imwrite("./save/1" + str(image_num) + ".jpg", crop_img)    # cropped 
			if(image_num % FPS):
				some = 1
				# print("")
			else:
				cv2.imwrite("./" + folder_name + "/"+ image_name + "_" + str(image_num) + ".jpg", frame)       # not cropped
				print (int(image_num / 30))
			#name     =  image_name + "_" + str(image_num) + ".jpg"
			#size     =  str(os.stat("./" + folder_name + "/" + name).st_size)
			#	,"_via_img_metadata":{},"_via_attributes":{"region":{},"file":{}}}
			image_num += 1
			'''
			cv2.rectangle(frame, (x-1, y-1), (x + w +2, y + h +2), (0, 255, 0), 1)
			
			# write as txt file
			name       = '"'+name+size+'"'
			filename   = '"filename":' + name
			size       = '"size":'     + size

			regions    = '[{"shape_attributes":{"name":"rect","x":'+str(x)+',"y":'+str(y)+',"width":'+str(w)+',"height":'+str(h)+'},"region_attributes":{}}]'
			region     = '"regions":'+regions 
			att        = '"file_attributes":{}}'

			line = ","+name+":{"+filename+","+size+","+region+","+att
			f.write(line)
			


			#write as json file for Darknet
			#filename =  args["video"]+str(size)
			#regions  =  [{"shape_attributes":{"name":"rect","x":str(x),"y":str(y),"width":str(w),"height":str(h)},"region_attributes":{"objectname":"guntest"}}]
			#line =     {   name:{ "filename":filename,"size":size,"regions":regions,"file_attributes":{} }  }
			#data['_via_img_metadata'].append( line )
			'''

		#cv2.putText(frame,"S - mark, C - cancel, Q - quit", (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255),1)
		# show the output frame
		pos = vs.get(cv2.CAP_PROP_POS_FRAMES)

		
		cv2.setTrackbarPos("Frame","Frame", int(pos))
		cv2.imshow("Frame", frame)

		key = cv2.waitKey(playSpeed) & 0xFF



		# if the 's' key is selected, we are going to "select" a bounding
		# box to track
		if key == ord("s"):
			try:
				# select the bounding box of the object we want to track (make
				# sure you press ENTER or SPACE after selecting the ROI)
				box = cv2.selectROI("Frame", frame, fromCenter=False,
					showCrosshair=True)

				# create a new object tracker for the bounding box and add it
				# to our multi-object tracker
				tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
				trackers.add(tracker, frame, box)

			except:
				print("maybe box too big")	
		

		if key == ord("c"):

			trackers = cv2.MultiTracker_create()

		# if the `q` key was pressed, break from the loop
		elif key == ord("q"):
			break
	except Exception as e:
		print("errror :{}".format(e))

#f.write("}")
if download == 1:
	answer = str(input("Download video? [Y/N] "))
	#print (answer)
	if answer == "y" or answer == "Y" :
		filename = play.download(filepath="./"+ str(folder_name) + "/")
		print ("Dowload video :" + filename)
	elif answer == "n" or answer == "N":
		print ("Video not download...")
	else:
		print ("Video not found....")
else:
	None

#with open('data.json',"w+") as outfile:
#     json.dump(data, outfile)

# if we are using a webcam, release the pointer
if not args.get("video", False):
	vs.stop()

# otherwise, release the file pointer
else:
	vs.release()

# close all windows
cv2.destroyAllWindows()
