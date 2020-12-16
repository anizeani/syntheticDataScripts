import cv2 
import numpy    
import csv

path = r"C:\Users\Eran\Documents\MLdataset\train"
# annotations = []
# with open(path + '/train_annotaions.csv', 'r') as f:
#     annotations = list(csv.reader(f, delimiter=','))
#     print(annotations)
# for image_file in glob.glob(path + '/*.jpg'):
#     cv2.imread(image_file)

# image = "1.jpg"
a = []
with open(path + "\\train_annotations.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row == []: continue
        image = row[0]
            # a.append(row)
        
        image_file = cv2.imread(path + "/" + image)
        if row[1] != "":
            cv2.rectangle(image_file, (int(row[1]), int(row[2])), (int(row[3]), int(row[4])), (13,0,100), 2)
            cv2.imshow("image", image_file)
            cv2.waitKey()

            # print(row)
            # a.append(row)

# image_file = cv2.imread(path + "/" + image)
# cv2.rectangle(image_file, (int(0.3884924*1280), int(0.2542411*800)), (int(0.4090403*1280), int(0.2951715*800)), (13,0,100), 2)
# cv2.rectangle(image_file, (int(100), int(200)), (int(200), int(300)), (13,0,100), 2)
# cv2.rectangle(image_file, (int(0.5965854*1280), int(0.6019815*800)), (int(0.6196514*1280), int(0.6330615*800)), (13,0,100), 2)
# cv2.rectangle(image_file, (int(0.1860677*1280), int(0.6004711*800)), (int(0.2095174*1280), int(0.637368*800)), (13,0,100), 2)

# what should be
print(image_file.shape)

for row in a:
    cv2.rectangle(image_file, (int(row[1]), int(row[2])), (int(row[3]), int(row[4])), (13,0,100), 2)
# cv2.rectangle(image_file, (int(0), int(0)), (int(10), int(10)), (13,0,100), 2)    
# what is
# cv2.rectangle(image_file, (int(125), int(208)), (int(137), int(221)), (13,0,100), 2)
# cv2.rectangle(image_file, (int(125), int(800-208)), (int(137), int(800-221)), (13,0,100), 2)

cv2.imshow("image", image_file)
cv2.waitKey()