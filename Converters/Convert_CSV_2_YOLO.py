import csv
from csv import reader
from tqdm import tqdm
import os.path

classes_coded = []
classes_names = []

# for l in csv.reader(open('class-descriptions-boxable.csv')):
#     # print(l)
#     classes_coded.append(l[0])
#     classes_names.append(l[1])
#     # break

# classes_coded.append(0)
# classes_names.append("human")

print(len(classes_names))

# 601 classes, not 600...

#
with open('DavosFlight4_all_annotations_thermal_retinaFormat.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        filename, file_extension = os.path.splitext(row[0])
        if row[1] == '': continue
        with open ("{}.txt".format(filename),'a') as f:
            height = (int(row[4])+int(row[2]))/550
            width = (int(row[3])-int(row[1]))/640
            centerY = (int(row[2])+int(row[4]))/(2*550)
            centerX = (int(row[1])+int(row[3]))/(2*640)
            f.write(f"0,{str(centerX)},{str(centerY)},{str(width)},{str(height)}\n")
        # row variable is a list that represents a row in csv

        print(row)
# print((0.4084495-0.02663646/2)*640)

# input_file = csv.DictReader(open("all_params_annotations.csv"))
# for line in tqdm(list(input_file)):
    # filename, file_extension = os.path.splitext(line[0])
#     with open ("{}.txt".format(filename)) as f:
#         f.write(f"0,{(line[1]+line[3])/(2*640)},{(line[2]+line[4])/(2*550)},{(line[3]-line[1])/640},{(line[4]+line[2])/550}")

# for line in tqdm(list(input_file)):
#     # print(line)
#     # print(line['LabelName'],classes_coded.index(line['LabelName']))
#     with open('train/%s.txt'%line['ImageID'],'w') as f:
#         f.write(','.join([str(classes_coded.index(line['LabelName'])),line['XMin'],line['YMin'],str(float(line['XMax'])-float(line['XMin'])),str(float(line['XMax'])-float(line['YMin']))])+'\n')
#     # break

# input_file = csv.DictReader(open("validation-annotations-bbox.csv"))

# for line in tqdm(list(input_file)):
#     # print(line)
#     # print(line['LabelName'],classes_coded.index(line['LabelName']))
#     with open('val/%s.txt'%line['ImageID'],'w') as f:
#         f.write(','.join([str(classes_coded.index(line['LabelName'])),line['XMin'],line['YMin'],str(float(line['XMax'])-float(line['XMin'])),str(float(line['XMax'])-float(line['YMin']))])+'\n')
#     # break