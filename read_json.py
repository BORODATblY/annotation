

import json
import cv2


folder = str('/Users/athenaimac/Desktop/annotation/weapon by name from drive/Ak/')

with open('/Users/athenaimac/Desktop/annotation/weapon by name from drive/Ak/AK.json') as json_file:
	data = json.load(json_file)

#for key, value in data['_via_img_metadata'].items():
#    print key, value['regions']


	
for key in data['_via_img_metadata']:

	#print(key)
	filename = data['_via_img_metadata'][key]['filename']
	print( filename )


	try:

		# read image from folder
		img = cv2.imread(folder + filename)
		height,width,c = img.shape
		print(height,width)

		f = open(folder + filename[:-4] + ".txt", "w")  # filename.split('.')[0]

		print(data['_via_img_metadata'][key]['regions'][0])
		print(len(data['_via_img_metadata'][key]['regions']))

		for params in range(0, len(data['_via_img_metadata'][key]['regions']) ):


			#cl = data['_via_img_metadata'][key]['regions'][0]['region_attributes']['Class']

			x = float( data['_via_img_metadata'][key]['regions'][params]['shape_attributes']['x'] )
			y = float( data['_via_img_metadata'][key]['regions'][params]['shape_attributes']['y'] )
			w = float( data['_via_img_metadata'][key]['regions'][params]['shape_attributes']['width'] )
			h = float( data['_via_img_metadata'][key]['regions'][params]['shape_attributes']['height'] )
			#print(x)

			f.write( str(5)+" "+ str( (x+w/2)/width )+" "+str(( y+h/2)/height )+" "+str( w/width )+" "+str( h/height ) ) 
			f.write(" \n")

			cv2.rectangle(img,(int(x),int(y)),(int(x+w),int(y+h)),(0,255,0),3)
		


		f.close() 

		cv2.imshow("frame",img)
		key = cv2.waitKey(1) & 0xFF
	except Exception as e:
		print("error kernel:{}".format(e))

