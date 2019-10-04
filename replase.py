import os


path = str(r'/Users/athenaimac/Desktop/annotation/mp 7/screenshot4/')
#folder_name = os.path.dirname(path)
listOfFiles = os.listdir(path)

countOfFiles = len(listOfFiles)

os.chdir(path)

for i in range(0, countOfFiles):
    os.rename(path+listOfFiles[i], 'sh' + str(i+1)+'.jpg')