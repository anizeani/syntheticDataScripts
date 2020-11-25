import numpy as np
import cv2


INPUT_PATH = "10_pink.jpg"
LABELS = "10.jpg_1_annotations_yolo.txt"
OUTPUT_PATH = "labels.jpg"


img = cv2.imread(INPUT_PATH)
shape = img.shape[:2]
total_height, total_width = shape
with open(LABELS, "r") as lbl:
    for line in lbl.read().splitlines():
        # for lable, rel_box_center_x, rel_box_center_y, rel_box_width, rel_box_height in  map(float, line.split()):
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

cv2.waitKey()
cv2.destroyAllWindows()
if __name__ == "__main__":



    pass