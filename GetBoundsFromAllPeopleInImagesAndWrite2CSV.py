import os
import writeCSVfromOpenCVBounds
import glob 
import cv2 as cv
import numpy as np
import random as rng
import pickle
import code

rng.seed(12345)

def isRectangleOverlap(R1, R2):
      if (R1[0]>=R2[0]+R2[2]) or (R1[0]+R1[2]<=R2[0]) or (R1[1]+R1[3]<=R2[1]) or (R1[1]>=R2[1]+R2[3]):
        return False
      else:
        return True

def takeMaxAndMinOfOverlappingRectanglesAndMerge(R1,R2):
    if R1[0] > R2[0]: minX = R2[0] 
    else: minX = R1[0]
    if R1[1] > R2[1]: minY = R2[1] 
    else: minY = R1[1]
    if R1[0] + R1[2] > R2[0] + R2[2]: width = R1[2] 
    else: width = R2[2]
    if R1[1] + R1[3] > R2[1] + R2[3]: height = R1[3] 
    else: height = R2[3]
    return (minX, minY, width, height)

def getAreaOfRect(Rect):
    return Rect[2]*Rect[3]

def GetBoundsFromAllPeople(path):
    # Convert image to hsv and set lower & upper bounds for mask
    # hsv_image = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    brighter_red = np.array([0, 120, 100])
    darker_red = np.array([10, 255, 255])
    second_brigth_red = np.array([170,120,255])
    second_dark_red = np.array([180,255,255])
    datasets = ['train/colored', 'test/colored']
    for ds in datasets:
        train_lable = []
        train_lable_without_empty_entries = []
        test_lable = []
        image_path = os.path.join(path, ds)
        for image_file_shader_people in glob.glob(image_path + '/*.jpg'):
            filename = os.path.basename(image_file_shader_people)
            filename = filename.replace('_pink','')
            # if "183_30" not in filename: continue
            # if "195_60" not in filename: continue
            shader_image = cv.imread(image_file_shader_people)
            # src_gray = cv.cvtColor(shader_image,cv.COLOR_BGR2GRAY)
            # cv.imshow("gray",src_gray)
            # cv.waitKey()
            # src_gray = cv.blur(src_gray,(3,3))
            # cv.imshow("grayBlurred",src_gray)
            # cv.waitKey()
            shader_image_HSV = cv.cvtColor(shader_image, cv.COLOR_BGR2HSV)
            # cv.imshow("original", shader_image)
            # cv.imshow("image_hsv", shader_image_HSV)
            mask1 = cv.inRange(shader_image_HSV, brighter_red, darker_red)
            mask2 = cv.inRange(shader_image_HSV,second_brigth_red,second_dark_red)
            mask1 = mask1 + mask2
            mask1 = cv.GaussianBlur(mask1,(5,5),1)
            shader_image = cv.GaussianBlur(shader_image,(3,3),1)
            # cv.imshow('mask',mask)
            filteredImage = cv.bitwise_and(shader_image, shader_image, mask = mask1)
            
            # cv.imshow("filteredImage",filteredImage)
            # cv.imshow("bluredImage",shader_image)
            # fileteredBluredImage = cv.blur(filteredImage,(3,3))   
            # cv.imshow("filteredImage",filteredImage)
            canny_output = cv.Canny(filteredImage, 100, 200)
            # cv.imshow("canny_output",canny_output)
            # cv.waitKey()

            image_height, image_width, _ = shader_image.shape
            contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL , cv.CHAIN_APPROX_NONE)
            
            if len(contours) == 0:
                if ds == 'train/colored':
                    train_lable.append([filename, '','','','',''])
                    continue
                else:
                    test_lable.append([filename, '','','','',''])
                    continue
            
            # contoursArea = []
            
            # for i,c in enumerate(contours):
            #     contoursArea.append(cv.contourArea(c))
            # maxSize = np.max(contoursArea)
            # removalIndices = []
            
            # pickle.dump(contours, open("contoursPreRemoval","wb"))
            # code.interact(local=locals(), banner="first")

            # for i, c in enumerate(contours):
            #     if cv.contourArea(c) < (maxSize/30): 
            #         removalIndices.append(i)

            # for i in reversed(removalIndices):
            #     del contours[i]

            contours_poly = [None]*len(contours)
            boundRect = [None]*len(contours)

            for i, c in enumerate(contours):
                contours_poly[i] = cv.approxPolyDP(c, 3, True)
                boundRect[i] = cv.boundingRect(contours_poly[i])

            ### 13.11: trying to group the rectangles close to eachother (debugging)

            # GROUP RECTANGLES, SOMEHOW STILL FAILS!
            # rectangles = []
            rectangles = boundRect
            # for i in range(len(contours)):
            #     rectangles.append([int(boundRect[i][0]), int(boundRect[i][1]), int(boundRect[i][2]), int(boundRect[i][3])]) 
            # if len(rectangles) > 1:
            #     rectangles, weights = cv.groupRectangles(rectangles,1,2)
            
            rectArea = []
            for rect in rectangles:
                rectArea.append(rect[2]*rect[3])  
            maxRectArea = np.max(rectArea)
            removalIndices = []
            for i, area in enumerate(rectArea):
                if area < (maxRectArea/4) :
                    removalIndices.append(i)
            for i in reversed(removalIndices):
                del rectangles[i]
            rectangles.sort(key = getAreaOfRect, reverse = True)

            # removeResidualRectangles = []
            # pairwiseOverlappingRects = []

            # for i in range(len(rectangles)):
            #     for j in range(i+1,len(rectangles)):
            #         # rectangles[:] = [rectangles[j] for rectangles[j] in rectangles if isRectangleOverlap(rectangles[i],rectangles[j])] 
            #         if isRectangleOverlap(rectangles[i],rectangles[j]): 
            #             pairwiseOverlappingRects.append(takeMaxAndMinOfOverlappingRectanglesAndMerge(rectangles[i],rectangles[j]))
            #             rectangles[i] = None
            #             rectangles[j] = None
            # for rect in rectangles:
            #     if (rect != None):
            #         pairwiseOverlappingRects.append(rect)
            
            # RectanglesAfterRemoval.append(takeMaxAndMinOfOverlappingRectanglesAndMerge())
            # for i in reversed(removeResidualRectangles):
            #     del rectangles[i]

            # pickle.dump(contours,open("contoursPastRemoval","wb"))
            # code.interact(local=locals(),banner="second")
            # drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
            # f = open(f"{imageNumber}_{tag}_annotations_yolo.txt","w")

            # for i in range(len(contours)):
            # for i in range(len(pairwiseOverlappingRects)):
            for i in range(len(rectangles)):
                color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
                cv.drawContours(shader_image, contours_poly, i, color)
                #if(boundRect[i][3] < 1): continue
                # cv.rectangle(shader_image, (int(boundRect[i][0]), int(boundRect[i][1])), \
                # (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
                
                # needed for grouping:
                # cv.rectangle(shader_image, (pairwiseOverlappingRects[i][0], pairwiseOverlappingRects[i][1]), (pairwiseOverlappingRects[i][0]+pairwiseOverlappingRects[i][2], pairwiseOverlappingRects[i][1]+pairwiseOverlappingRects[i][3]), color, 2)
                cv.rectangle(shader_image, (int(rectangles[i][0]), int(rectangles[i][1])), (int(rectangles[i][0]+rectangles[i][2]), int(rectangles[i][1]+rectangles[i][3])), color, 2)
                # cv.imshow(filename,shader_image)
                # cv.imshow(filename + " canny",canny_output)
                # cv.imshow(filename + "mask", mask1)
                # cv.waitKey()
                if ds == 'train/colored':
                    # train_lable.append([filename,int(boundRect[i][0]), int(boundRect[i][1]), int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3]),'human'])
                    train_lable.append([filename,rectangles[i][0], rectangles[i][1], rectangles[i][0]+boundRect[i][2], rectangles[i][1]+rectangles[i][3],'human'])
                    train_lable_without_empty_entries.append([filename,rectangles[i][0], rectangles[i][1], rectangles[i][0]+boundRect[i][2], rectangles[i][1]+rectangles[i][3],'human'])
                    print(f"{filename} is appended to train_lable")
                else: 
                    # test_lable.append([filename,int(boundRect[i][0]), int(boundRect[i][1]), int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3]),'human'])
                    test_lable.append([filename,rectangles[i][0], rectangles[i][1], rectangles[i][0]+boundRect[i][2], rectangles[i][1]+rectangles[i][3],'human'])
                    print(f"{filename} is appended to test_lable")
                # k = cv.waitKey()
                # if k == 27:
                #     exit(0)
            if ds == 'train/colored':
                writeCSVfromOpenCVBounds.createCSVfromBounds("label_train.csv",train_lable)
                writeCSVfromOpenCVBounds.createCSVfromBounds("label_train_for_anchor_optimization.csv",train_lable_without_empty_entries)
            else: writeCSVfromOpenCVBounds.createCSVfromBounds("label_test.csv",test_lable)
if __name__ == "__main__":
    GetBoundsFromAllPeople(os.getcwd())
else:
    #get the absolute path of the file no matter what your current dir is (from other file) needs to be tested
    GetBoundsFromAllPeople(os.path.dirname(os.path.abspath(__file__))) 
    pass