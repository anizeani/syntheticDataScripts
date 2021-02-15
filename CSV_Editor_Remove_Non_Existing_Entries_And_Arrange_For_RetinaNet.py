import csv
import os
import cv2

# from sys import argv
from tkinter.filedialog import askdirectory
path = askdirectory()

class csvEditor:
    def __init__(self,csv_file_path):
        self.csv_file_path = csv_file_path
        self.idealFormat = False
        self.removalList = list()
        self.csvAsList = list()
        with open (csv_file_path + '//all_annotations_thermal.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if row[0] == "timestamp_ns": continue
                fileEnding = row[0].split(".")
                if len(fileEnding) == 2 & len(row) == 6:
                    self.idealFormat == True
                    image = row[0]
                # if ideal_csv_format == True:
                #     image = row[0]
                else: image = row[0] + ".png" 
                image_file = cv2.imread(self.csv_file_path + "/" + image)
                if(image_file is None):
                    self.removalList.append(row)
                else: self.csvAsList.append(row) 

    def removeRowFromCSV(self):
        listForEditingCSV = list()
        tempList = list()
        with open(self.csv_file_path + '//all_annotations_thermal.csv','r') as readFile: #if using with, no need to close file in the end
            reader = csv.reader(readFile)
            for ROW in reader:
                if ROW[0] == "timestamp_ns": continue
                listForEditingCSV.append(ROW)
                tempList.append(ROW)
        for member in listForEditingCSV:
            if member in self.removalList:
                tempList.remove(member) # Hint: don't remove from the same list you iterate over... it's difficult to follow.. some index problems.. better keep a temporary copy list and edit that one
        with open(self.csv_file_path + "\\annotations_nonExistingImagesRemoved.csv",'a',newline='') as writeFile:
            writeFile.truncate(0)
            writer = csv.writer(writeFile)
            writer.writerows(tempList)

    def createCleanCSV(self):
        with open(self.csv_file_path + '\\annotations_nonExistingImagesRemoved.csv','r') as readFile: #if using with, no need to close file in the end
            reader = csv.reader(readFile)
            lines = list()
            for row in reader:
                if row[0] == "timestamp_ns": continue
                if self.idealFormat == False: #the id is after the image name, .png is missing, and width and height instead of pixel locations left up and bottom right for bounding box
                    headers = [row[0]+".png",row[2],row[3],int(row[2]) + int(row[4]), int(row[3]) + int(row[5]), "human"]
                else: headers = [row[0],row[1],row[2],row[3],row[4],"human"]
                lines.append(headers)
            with open(self.csv_file_path + "//annotations_thermal_clean.csv", 'a', newline='') as write:
                    write.truncate(0)
                    writer = csv.writer(write)
                    writer.writerows(lines) 
        self.idealFormat = True

# path = r"C:\Users\Eran\Desktop\final_split_Train_Test_Humans\testLaying\train"

# if "path" in argv:
#     path = argv[-1]
# else: exit(1)

# path = os.getcwd()
# is_csv_ideal_Format = True
foo = csvEditor(path)
foo.removeRowFromCSV()
if foo.idealFormat is not True: foo.createCleanCSV()