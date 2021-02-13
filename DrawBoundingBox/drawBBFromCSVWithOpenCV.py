import cv2 
import numpy    
import csv
import os

# def removeRowFromCSV(path,removalList):
#     listForEditingCSV = list()
#     tempList = list()
#     with open(path + '//all_annotations_thermal.csv','r') as readFile: #if using with, no need to close file in the end
#         reader = csv.reader(readFile)
#         for ROW in reader:
#             listForEditingCSV.append(ROW)
#             tempList.append(ROW)
#     for member in listForEditingCSV:
#         if member in removalList:
#             tempList.remove(member) # Hint: don't remove from the same list you iterate over... it's difficult to follow.. some index problems.. better keep a temporary copy list and edit that one
#     with open(path + "\\edited_annotations.csv",'r+',newline='') as writeFile:
#         writeFile.truncate()
#         writer = csv.writer(writeFile)
#         writer.writerows(tempList)

# path = r"C:\Users\Eran\Desktop\rosbagFiles\davos_flight2_ir\imagesWithAnnotations"
# path = r"C:\Users\Eran\Desktop\final_split_Train_Test_Humans\real_background"
# path = r"C:\Users\Eran\Desktop\final_split_Train_Test_Humans\testSet"
path = r"C:\Users\Eran\Desktop\rosbagFiles\davosFlight4_flir\backgound_flight4"
# annotations = []
# with open(path + '/train_annotaions.csv', 'r') as f:
#     annotations = list(csv.reader(f, delimiter=','))
#     print(annotations)
# for image_file in glob.glob(path + '/*.jpg'):
#     cv2.imread(image_file)

# image = "1.jpg"
a = []
counter = 0
idealFormat = False

removalList = list()
iterate = 0

# with open(path + "\\test.csv") as csv_file:
# with open(path + "\\all_annotations_thermal.csv") as csv_file:
with open(path + "\\DavosFlight4_all_annotations_thermal.csv") as csv_file:
    
    # for row in csv_file:
    #     b.append(row)
    
    csv_reader = csv.reader(csv_file)

    # for row in csv_reader:
    #     c.append(row)

    for row in csv_reader:
        iterate += 1
        if row[0] == "timestamp_ns": continue
        if row == []: continue
        if idealFormat == True:
            image = row[0]
        else: image = row[0] + ".png"

        # a.append(row)
        image_file = cv2.imread(path + "/" + image)
        # if(image_file is None):
        #     removalList.append(row)
        if(image_file is not None):
            if row[1] != "":
                if idealFormat == True:
                    topLeftCorner = (int(row[1]), int(row[2]))
                    bottomRightCorner = (int(row[3]), int(row[4]))
                    cv2.rectangle(image_file, topLeftCorner, bottomRightCorner, (255,0,0), 2)
                    counter += 1
                    print("image: " + image)
                    print(row)
                    print(topLeftCorner, bottomRightCorner)
                    cv2.imshow("image", image_file)
                    cv2.waitKey()
                    
                else:
                    # os.getcwd()
                    counter += 1
                    topLeftCorner = (int(row[2]), int(row[3]))
                    bottomRightCorner = (int(row[2]) + int(row[4]), int(row[3]) + int(row[5]))
                    # cv2.imwrite(path + "\\imagesWithAnnotations\\" + image,image_file) 
                    cv2.rectangle(image_file, topLeftCorner, bottomRightCorner, (255,0,0), 2)
                    # cv2.rectangle(image_file, (5,5),( 20,20 ), (255,0,0), 2)
                    headers = [row[0]+".png",row[2],row[3],int(row[2]) + int(row[4]), int(row[3]) + int(row[5])]
                    # with open(r'annotation_standing.csv', 'a', newline='') as f:
                    #     writer = csv.writer(f)
                    #     writer.writerow(headers)
                    print("image: " + image)
                    print(row)
                    print(topLeftCorner, bottomRightCorner)

                    cv2.imshow("image", image_file)
                    cv2.waitKey()
                    os.remove(path + "\\" + image)
            # print(row)
            # a.append(row)
print('amount of detections: '+ str(counter))
print(iterate)
# removeRowFromCSV(path, removalList)








# image_file = cv2.imread(path + "/" + image)
# cv2.rectangle(image_file, (int(0.3884924*1280), int(0.2542411*800)), (int(0.4090403*1280), int(0.2951715*800)), (13,0,100), 2)
# cv2.rectangle(image_file, (int(100), int(200)), (int(200), int(300)), (13,0,100), 2)
# cv2.rectangle(image_file, (int(0.5965854*1280), int(0.6019815*800)), (int(0.6196514*1280), int(0.6330615*800)), (13,0,100), 2)
# cv2.rectangle(image_file, (int(0.1860677*1280), int(0.6004711*800)), (int(0.2095174*1280), int(0.637368*800)), (13,0,100), 2)

# what should be
# print(image_file.shape)

# for row in a:
#     cv2.rectangle(image_file, (int(row[1]), int(row[2])), (int(row[3]), int(row[4])), (13,0,100), 2)
# cv2.rectangle(image_file, (int(0), int(0)), (int(10), int(10)), (13,0,100), 2)    
# what is
# cv2.rectangle(image_file, (int(125), int(208)), (int(137), int(221)), (13,0,100), 2)
# cv2.rectangle(image_file, (int(125), int(800-208)), (int(137), int(800-221)), (13,0,100), 2)

# cv2.imshow("image", image_file)
# cv2.waitKey()


