import cv2

# font = cv2.FONT_HERSHEY_SIMPLEX

# cv2.rectangle(outImg,(50, 200),(150, 50),(100,0,0),2)
# cv2.putText(outImg,"Colors: " + "red",(50+10, 200+20),font, 0.5, (0,0,0), 1, cv2.LINE_AA)

# cv2.imwrite("outputTest.jpg", outImg)

# print("done")

# For bounding box

def drawPrettyBox(xmin, xmax, ymin, ymax, label, imgPath):
    
    color = (200,0,0)
    text_color = (255,255,255)
    
    outImg = cv2.imread(imgPath)
    cv2.rectangle(outImg, (xmin, ymax), (xmax, ymin), color, 2)
    
    # For the text background
    # Finds space required by the text so that we can put a background with that amount of width.
    (w, h), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)

    # Prints the text.    
    cv2.rectangle(outImg, (xmin, ymax - 20), (xmin + w, ymax), color, -1)
    cv2.putText(outImg, label, (xmin, ymax - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1)


    cv2.imwrite(imgPath, outImg)


