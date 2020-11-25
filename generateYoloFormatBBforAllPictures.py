for filename in os.listdir(os.getcwd()):
    if filename == '.vscode': continue
    if '_annotated' in filename: 
        continue
    OUTPUT_PATH, b = os.path.splitext(filename)
    if b == '.jpg':
        if '_pink' in filename:
            imageNumber = filename.replace('_pink','')
            brighter_red = np.array([-100, 100, 100])
            darker_red = np.array([20, 255, 255])

            # brightmagenta:
            lower_magenta = np.array([100, 100, 100])
            #darkmagenta:
            upper_magenta = np.array([200, 255, 255])
            # mask = cv.inRange(hsv_image, lower_magenta, upper_magenta)
            tag = 0
            createTxtForYoloFormat(tag, src, brighter_red,darker_red,imageNumber)

            # cyan = np.uint8([[[139,0,139]]])
            # cyan_hsv = cv.cvtColor(cyan, cv.COLOR_BGR2HSV)
            # print(cyan_hsv)
            lower_cyan = np.array([50, 100, 100])
            upper_cyan = np.array( [150, 255, 255])
            tag = 1
            createTxtForYoloFormat(tag, src, lower_cyan,upper_cyan,imageNumber)

def createTxtForYoloFormat(tag, originalImage, lowerColorThresh, higherColorThresh, imageNumber):
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
    
    
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    
    f = open(f"{imageNumber}_{tag}_annotations_yolo.txt","w")
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
        f.write(f"{tag} {normalizedCenterX} {normalizedCenterY} {normalizedBBWidth} {normalizedBBHeight} \n")  
    cv.imshow(f'{tag}_ContourAnd_BB_AfterFiltering', drawing)