import cv2 
import numpy    
import csv

path = r"C:\Users\Eran\Documents\MLdataset\train"

image = "3061.jpg"
image_file = cv2.imread(path + "/" + image)
with open(path + "\\train_annotations.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row == []: continue
        if row[0] == image:    
            image_file = cv2.imread(path + "/" + image)
            if row[1] != "":
                cv2.rectangle(image_file, (int(row[1]), int(row[2])), (int(row[3]), int(row[4])), (13,0,100), 2)
                cv2.imshow("image", image_file)
                cv2.waitKey()