import cv2 as cv
import numpy as np

def rgbToHSV(color, r,g,b):
    colorNumpy = np.uint8([[[r,g,b]]])
    color_To_HSV = cv.cvtColor(colorNumpy, cv.COLOR_BGR2HSV)
    print(f"the color {color} in hsv is: {color_To_HSV}")

rgbToHSV("cyan", 110,200,179)
rgbToHSV("darkred",175,32,19)