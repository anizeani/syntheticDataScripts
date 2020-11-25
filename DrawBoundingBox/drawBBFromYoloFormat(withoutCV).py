import numpy as np
import cv2
import glob
import os

## place the script into the same folder as the images (.jpg) and the labels (.txt) are
## annotated output will be generated with the _annotated.jpg ending
## press space to iterate through images
## press escape (key 27) to quit 
## to just annotate without preview, comment cv2.imshow & the if cv2.waitkey() out

for filename in os.listdir(os.getcwd()):
    if filename == '.vscode': continue
    if '_annotated' in filename: 
        continue
    OUTPUT_PATH, b = os.path.splitext(filename)
    OUTPUT_PATH += "_annotated.jpg"
    if b == '.jpg': INPUT_PATH = filename
    for label in os.listdir(os.getcwd()):
        if os.path.splitext(filename)[0] == os.path.splitext(label)[0]:
            if os.path.splitext(label)[1] == '.txt': 
                LABELS = label
                break
    img = cv2.imread(INPUT_PATH)
    shape = img.shape[:2]
    total_height, total_width = shape
    with open(LABELS, "r") as lbl:
        for line in lbl.read().splitlines():
            #[rel_box_center_x, rel_box_center_y, rel_box_width, rel_box_height] = line.split()

            label, rel_box_center_x, rel_box_center_y, rel_box_width, rel_box_height = [float(f) for f in line.split()]
            box_center_x = rel_box_center_x * total_width
            box_center_y = rel_box_center_y * total_height
            box_width = total_width * rel_box_width
            box_height = total_height * rel_box_height
            size = np.array([box_width, box_height])
            start = np.array([box_center_x, box_center_y]) - (size/2)
            img = cv2.rectangle(img, [*start, *size], (0xff, 0, 0), 1)

    cv2.imwrite(OUTPUT_PATH, img)
    cv2.imshow("frame", img)
    if cv2.waitKey() == 27:
        break
cv2.destroyAllWindows()
