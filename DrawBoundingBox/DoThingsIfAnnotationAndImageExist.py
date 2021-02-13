import cv2 
import numpy    
import csv
import os

path = r"C:\Users\Eran\Desktop\final_split_Train_Test_Humans\flight2StandingHumans"
# path = r"C:\Users\Eran\Desktop\rosbagFiles\davos_flight2_ir\imagesWithAnnotations"

with open(path + "\\edited_annotations.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row[0] == "timestamp_ns": continue
        # if row == []: continue
        image = row[0] + ".png"
            # a.append(row)
        image_file = cv2.imread(path + "/" + image)
        if(image_file is not None):
            if row[1] != "":
                # os.getcwd()
                topLeftCorner = (int(row[2]), int(row[3]))
                bottomRightCorner = (int(row[2]) + int(row[4]), int(row[3]) + int(row[5]))

                headers = [row[0]+".png",row[2],row[3],int(row[2]) + int(row[4]), int(row[3]) + int(row[5])]
                with open(path + '\\annotation_standing_flight2.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                f.close()

                # counter += 1
                # cv2.imwrite(path + "\\imagesWithAnnotations\\" + image,image_file) 
                cv2.rectangle(image_file, topLeftCorner, bottomRightCorner, (255,0,0), 2)
                # cv2.rectangle(image_file, (5,5),( 20,20 ), (255,0,0), 2)
                
                print("image: " + image)
                print(row)
                print(topLeftCorner, bottomRightCorner)


def deleteImage(image):
    os.remove(path + "\\" + image)