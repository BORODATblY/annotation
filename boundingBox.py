import json
import cv2
import os
import shutil

#image
imgpass = os.path.dirname('/Users/athenaimac/Desktop/m16/m16_output/vott-json-export')
#create new foldet target image \Users\andri\Downloads\AK-47\new\\

newpass = os.path.dirname('/Users/athenaimac/Desktop/m16/m16_output_cln')
#json
jsnpass = os.path.dirname('/Users/athenaimac/Desktop/m16/m16_output')
os.chdir(jsnpass)
jsn = os.listdir()
for j in jsn:
    try:
        with open(jsnpass + '/' + j) as json_file:
            data = json.load(json_file)
        filename = str(data['asset']['name']) + '.jpg'
        frame = cv2.imread(imgpass + '/' + filename)
        height,width,c = frame.shape


        tag = data['regions'][0]['tags']
        print(tag)


        # y = data['regions'][0]['boundingBox']['left']
        # x = data['regions'][0]['boundingBox']['top']
        # w = data['regions'][0]['boundingBox']['width']
        # h = data['regions'][0]['boundingBox']['height']
        #
        # print(str(cl) + " " + str((x + w / 2) / width) + " " + str((y + h / 2) / height) + " " + str(w / width) + " " + str(h / height))
        #
        #
        # box = []
        # box.append((x + w / 2) / width)
        # box.append((y + h / 2) / height)
        # box.append(w / width)
        # box.append(h / height)
        #
        # x1, y1 = int((box[0] + box[2] / 2) * w), int((box[1] + box[3] / 2) * h)
        # x2, y2 = int((box[0] - box[2] / 2) * w), int((box[1] - box[3] / 2) * h)

        x1 = int(data['regions'][0]['points'][0]['x'])
        y1 = int(data['regions'][0]['points'][0]['y'])
        x2 = int(data['regions'][0]['points'][2]['x'])
        y2 = int(data['regions'][0]['points'][2]['y'])
        print(filename)

        cv2.namedWindow("{}".format(filename), cv2.WINDOW_NORMAL)
        cv2.resizeWindow("{}".format(filename), 1024, 768)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.imshow("{}".format(filename), frame)
        key = cv2.waitKey(0) & 0xFF
        shutil.move(imgpass + '/' + filename, newpass + '/')

    except:
        pass
