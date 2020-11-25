from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
import random as rng
import writeCSVfromOpenCVBounds

rng.seed(12345)

def thresh_callback(val):
    threshold = val
    cv.imshow('result',res)
    canny_output = cv.Canny(res, threshold, threshold * 2)
    cv.imshow('dam',canny_output)
    cv.imwrite('cannyOutput.png',canny_output)
    contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    
    
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
        centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])
    
    
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    
    f = open("boundingboxesCoordinatesNormalized.txt","w")
    for i in range(len(contours)):
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv.drawContours(drawing, contours_poly, i, color)
        if(boundRect[i][3] < 10): continue
        cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
        (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
        normalizedCenterX = (boundRect[i][0] + boundRect[i][2]/2) / (width)
        normalizedCenterY = (boundRect[i][1]+boundRect[i][3]/2) / (height)
        normalizedBBWidth = boundRect[i][2] / width
        normalizedBBHeight = boundRect[i][3] / height
        f.write(f"{tag} {normalizedCenterX} {normalizedCenterY} {normalizedBBWidth} {normalizedBBHeight} \n")   
        # cv.waitKey()
        # cv.imshow('Contours', drawing)
        #cv.circle(drawing, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)
    cv.imshow('Contours', drawing)


def createTxtForYoloFormat(tag, originalImage, lowerColorThresh, higherColorThresh, threshold):
    image_HSV = cv.cvtColor(originalImage, cv.COLOR_BGR2HSV)
    cv.imshow("original", originalImage)
    cv.imshow("image_hsv", image_HSV)
    mask = cv.inRange(image_HSV, lowerColorThresh, higherColorThresh)
    cv.imshow('mask',mask)
    filteredImage = cv.bitwise_and(originalImage, originalImage, mask = mask)
    fileteredBluredImage = cv.blur(filteredImage,(3,3))   
    cv.imshow("filteredImage",filteredImage)
    canny_output = cv.Canny(fileteredBluredImage, 10, 80)
    cv.imshow("canny_output",canny_output)
    cv.waitKey()
    image_height, image_width, _ = originalImage.shape

    contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
        centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])
    createTxtForYoloFormat(filename,boundRect)
    
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    
    f = open(f"192_pink_annotations_yoloFormat.txt","w")
    for i in range(len(contours)):
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv.drawContours(drawing, contours_poly, i, color)
        #if(boundRect[i][3] < 1): continue
        cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
        (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
        normalizedCenterX = (boundRect[i][0] + boundRect[i][2]/2) / (image_width)
        normalizedCenterY = (boundRect[i][1]+boundRect[i][3]/2) / (image_height)
        normalizedBBWidth = boundRect[i][2] / image_width
        normalizedBBHeight = boundRect[i][3] / image_height
        f.write(f"{normalizedCenterX} {normalizedCenterY} {normalizedBBWidth} {normalizedBBHeight} \n")  
    cv.imshow(f'{tag}_ContourAnd_BB_AfterFiltering', drawing)

parser = argparse.ArgumentParser(description='Code for Creating Bounding boxes and circles for contours tutorial.')
parser.add_argument('--input', help='Path to input image.', default='192_pink.jpg')     
args = parser.parse_args()
src = cv.imread(cv.samples.findFile(args.input))

height, width, _ = src.shape 

if src is None:
    print('Could not open or find the image:', args.input)
    exit(0)

# Convert image to hsv and set lower & upper bounds for mask
# hsv_image = cv.cvtColor(src, cv.COLOR_BGR2HSV)
brighter_red = np.array([-100, 100, 100])
darker_red = np.array([20, 255, 255])

# brightmagenta:
lower_magenta = np.array([100, 100, 100])
#darkmagenta:
upper_magenta = np.array([200, 255, 255])
# mask = cv.inRange(hsv_image, lower_magenta, upper_magenta)
tag = 0
# createTxtForYoloFormat(tag, src, brighter_red,darker_red,100)

# cyan = np.uint8([[[139,0,139]]])
# cyan_hsv = cv.cvtColor(cyan, cv.COLOR_BGR2HSV)
# print(cyan_hsv)
lower_cyan = np.array([50, 100, 100])
upper_cyan = np.array( [150, 255, 255])
tag = 1
createTxtForYoloFormat(tag, src, lower_cyan,upper_cyan,100)
# for women: cyan (turkoise) will be used

# Threshold the HSV image to get only magenta colors
# print(cv.cvtColor(cv.color_green)



# Bitwise-AND mask and original image
# res = cv.bitwise_and(src, src, mask = mask)
# res = cv.blur(res, (3,3))
# source_window = 'Source'
# cv.namedWindow(source_window)
# cv.imshow(source_window, src)
# max_thresh = 255
# thresh = 100 # initial threshold
# cv.createTrackbar('Canny thresh:', source_window, thresh, max_thresh, thresh_callback)
# thresh_callback(thresh)
# cv.waitKey()