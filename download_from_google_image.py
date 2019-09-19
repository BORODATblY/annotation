from google_images_download import google_images_download
import sys
import json
import re
import os
from PIL import Image


'''
try:
    if not os.path.exists("image_download"): 
        os.makedirs("image_download") 
       
except OSError:
    print ('Error: Creating directory of save')

orig_stdout = sys.stdout
f = open('URLS.txt', 'w')
sys.stdout = f
'''
response = google_images_download.googleimagesdownload()   #class instantiation


arguments = {
			"keywords":"rifle in hands, mgun in hands, assault rifle in hands, rifle control, sniper rifle in hands, air rifles in hands, holding maghine gun, holding rifles, sniper rifle in the hands, machine gun in the hands, assault riflein the hands",
			"limit": 100,
			"size":'>1024*768',
			"format":'jpg', 
			"print_urls":True
		}

			#creating list of arguments


paths = response.download(arguments)   #passing the arguments to the function
"""
img_dir = ("./download/ " + arguments.keywords + "/")
for filename in os.listdir(img_dir):
    try :
        with Image.open(img_dir + "/" + filename) as im:
             print('ok')
    except :
        print(img_dir + "/" + filename)
        os.remove(img_dir + "/" + filename)
"""
print(paths)   #printing absolute paths of the downloaded images

