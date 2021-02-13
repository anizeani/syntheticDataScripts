#change margins of BB

import csv
import os

path = r"C:\Users\Eran\Documents\MLdataset\train"

train = '\\train_annotations.csv'
valid = '\\validation_annotations.csv'
train_anchor = '\\train_annotationsWithoutEmptyEntriesForAnchorOptimization.csv'
valid_anchor = '\\validation_annotationsWithoutEmptyEntriesForAnchorOptimization.csv'
annotations = [train, valid, train_anchor, valid_anchor]

margin = 2

for annotationCSV in annotations:
    lines = list()
    with open(path  + annotationCSV, 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if (len(row) > 2 & len(row[1]) !=0):
                row[1] = str(int(row[1]) + margin) #xmin x1
                row[2] = str(int(row[2]) + margin) #ymin y1
                row[3] = str(int(row[3]) - margin) #xmax x2
                row[4] = str(int(row[4]) - margin) #ymax y2
                lines.append(row)

    with open(path + "\\changedMargins" + annotationCSV, 'w', newline='') as writeFile:

        writer = csv.writer(writeFile)

        writer.writerows(lines)
