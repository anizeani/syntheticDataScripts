import csv
import os


path = r"C:\Users\Eran\Documents\MLdataset\train"

train = '\\train_annotations.csv'
valid = '\\validation_annotations.csv'
train_anchor = '\\train_annotationsWithoutEmptyEntriesForAnchorOptimization.csv'
valid_anchor = '\\validation_annotationsWithoutEmptyEntriesForAnchorOptimization.csv'
annotations = [train, valid, train_anchor, valid_anchor]

for annotationCSV in annotations:
    lines = list()
    with open(path  + annotationCSV, 'r') as readFile:
        reader = csv.reader(readFile)
        # print(os.getcwd())
        # print(os.path.dirname(os.path.realpath(__file__)))
        if annotationCSV == train_anchor: 
            print(lines) 
        for row in reader:
            if annotationCSV == train_anchor or annotationCSV == valid_anchor:
                if len(row[1]) == 0:
                    continue
            if len(row) > 2:
                lines.append(row)

    with open(path  + annotationCSV, 'w', newline='') as writeFile:

        writer = csv.writer(writeFile)

        writer.writerows(lines)