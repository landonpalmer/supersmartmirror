from platform import mac_ver
import cv2
def CompareBounds(H, S, V, upper_bound, lower_bound):
    if H <= upper_bound[0] and H >= lower_bound[0]:
            if S <= upper_bound[1] and S >= lower_bound[1]:
                if V <= upper_bound[2] and V >= lower_bound[2]:
                    return True
    return False

def DetermineColor(H, S, V):
    color_dict_HSV = {'black': [[180, 255, 30], [0, 0, 0]],
              'white': [[180, 18, 255], [0, 0, 231]],
              'red1': [[180, 255, 255], [159, 50, 70]],
              'red2': [[9, 255, 255], [0, 50, 70]],
              'green': [[89, 255, 255], [36, 50, 70]],
              'blue': [[128, 255, 255], [90, 50, 70]],
              'yellow': [[35, 255, 255], [25, 50, 70]],
              'purple': [[158, 255, 255], [129, 50, 70]],
              'orange': [[24, 255, 255], [5, 143, 0]],
              'gray': [[180, 18, 230], [0, 0, 40]],
              'beige': [[23,255,227], [12,44,30]]
              }
    new_color_dict_HSV = {
        'red': [[-10, 245, 164], [10, 265, 244]],
        'red-orange': [[9,255,255],[3,184,105]],
        'orange': [[15,255,255],[10,143,0]],
        'yellow-orange': [[28,255,255],[18,145,0]],
        'yellow': [[32,255,255],[25,122,0]],
        'green': [[74,255,255],[42,122,0]],
        'blue' : [[122,255,255],[83,118,0]],
        'violet': [[166,255,255],[125,109,0]],
        'white': [[180,40,255],[0,0,231]],
        'black': [[179,255,58],[0,0,0]],
        'gray': [[180, 18, 230], [0, 0, 40]],
        'beige': [[23,255,227], [12,44,30]]
    }
    for color in new_color_dict_HSV:
        upper_bound = new_color_dict_HSV[color][0]
        lower_bound = new_color_dict_HSV[color][1]
        if (CompareBounds(H, S, V, upper_bound, lower_bound)):
            # if (color == "red1") or (color == "red2"):
            #     return "red"
            return color
    return "unknown"

def ColorDetectionPipe(xmin, xmax, ymin, ymax, picturePath, outputPath):
    shrinkerx = int((xmax - xmin)*.10)
    shrinkery = int((ymax - ymin)*.10)
    xmin+=shrinkerx
    xmax-=shrinkerx
    ymin+=shrinkery
    ymax-=shrinkery

   
    img = cv2.imread(picturePath)    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = cv2.rectangle(img,(xmin, ymax),(xmax, ymin),(255,255,0),1)
    color_dict_scores = {
        'red': 0,
        'red-orange': 0,
        'orange': 0,
        'yellow-orange': 0,
        'yellow': 0,
        'green': 0,
        'blue': 0,
        'violet': 0,
        'white': 0,
        'black': 0,
        'gray': 0,
        'beige': 0,
        'unknown': 0, 
    }
    for i in range(xmin,xmax, 1):
        for j in range(ymin,ymax, 1):
            pixel = img[j,i]
            color = DetermineColor(pixel[0],pixel[1],pixel[2])
            color_dict_scores[color] += 1
    
    unknown_value = color_dict_scores["unknown"]
    del color_dict_scores['unknown']
    primary_color = max(color_dict_scores, key=color_dict_scores.get)
    secondary_color = sorted(color_dict_scores, key=color_dict_scores.get)[-2]
    for color in color_dict_scores:
        print(color + ": " + str(color_dict_scores[color]))
            
    print("----")

    font = cv2.FONT_HERSHEY_SIMPLEX
    outImg = cv2.imread(outputPath)
    cv2.rectangle(outImg,(xmin, ymax),(xmax, ymin),(255,255,0),1)
    cv2.putText(outImg,"primary color: " + primary_color,(xmin+10, ymax+20),font, 1.0, (0,0,0), 1, cv2.LINE_AA)

    # Only returns secondary color if it is greater than 15% of primary color
    primaryScore = color_dict_scores[primary_color]
    secondaryScore = color_dict_scores[secondary_color]
    
    primary_color_return = (primary_color, primaryScore)
    secondary_color_return = (secondary_color, secondaryScore)

    if secondaryScore > (primaryScore * 0.15):
        cv2.putText(outImg,"secondary_color: " + secondary_color,(xmin+10, ymax+40),font, 1.0, (0,0,0), 1, cv2.LINE_AA)
        
        cv2.imwrite(outputPath, outImg)

        cv2.destroyAllWindows()

        return [primary_color, secondary_color]
    
    # Save the cv2 img
    cv2.imwrite(outputPath, outImg)
    cv2.destroyAllWindows()

    return [primary_color]



    # return [primary_color_return,secondary_color_return, ("unknown", unknown_value)]


