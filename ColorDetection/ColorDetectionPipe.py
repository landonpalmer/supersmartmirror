from platform import mac_ver
import cv2
import os
import sys
from PIL import Image


def get_parent_dir(n=1):
    """returns the n-th parent dicrectory of the current
    working directory"""
    current_path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(n):
        current_path = os.path.dirname(current_path)
    return current_path

utils_path = os.path.join(get_parent_dir(1), "Utils")
sys.path.append(utils_path)

from utils import draw_annotated_box

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
    cv2.rectangle(outImg, (xmin, ymax - 20), (xmin + w, ymax), text_color, 1)
    


    cv2.imwrite(imgPath, outImg)


def CompareBounds(H, S, V, upper_bound, lower_bound):
    if H <= upper_bound[0] and H >= lower_bound[0]:
            if S <= upper_bound[1] and S >= lower_bound[1]:
                if V <= upper_bound[2] and V >= lower_bound[2]:
                    return True
    return False

def DetermineColor(H, S, V):
    if (V <= 40):
        return "black"
    if CompareBounds(H,S,V, [179,46,162],[0,0,0]):
        return "gray"
    if CompareBounds(H,S,V,[255,37,255],[0,0,173]):
        return "white"
    color_dict_HSV = {
        'red1': [[3,255,255],[0,132,0]],
        'red-orange': [[16,255,255],[4,59,0]],
        'orange': [[22,255,255],[17,68,0]],
        'yellow-orange': [[27,255,255],[23,56,0]],
        'yellow': [[36,255,255],[28,44,0]],
        'yellow-green' : [[56,255,255],[37,44,0]],
        'green': [[81,255,255],[57,44,0]],
        'blue-green' : [[100,255,255],[82,44,0]],
        'blue' : [[127,255,255],[101,41,0]],
        'blue-violet' : [[136, 255,255],[128, 15, 0]],
        'violet': [[154,255,255],[137,15,0]],
        'red-violet': [[162,255,255],[155,7,0]],
        'red2' : [[179,255,255],[163,38,0]],
    }
    for color in color_dict_HSV:
        upper_bound = color_dict_HSV[color][0]
        lower_bound = color_dict_HSV[color][1]
        if (CompareBounds(H, S, V, upper_bound, lower_bound)):
            if (color == "red1") or (color == "red2"):
                return "red"
            # if color == "blue-green":
            #     return "green"
            return color
    return "unknown"

# def DetermineColor(H,S,V):

#     # check for black
#     if V < 20:
#         return 'black'
    
#     # check for white
#     if V > 230:
#         return 'white'
    
#     # check for gray
#     if S < 50:
#         return 'gray'
    

#     color_dict = {
#         'red': [0, 177.5, 177.5],
#         'red-orange': [11, 177.5, 177.5],
#         'orange': [19, 177.5, 177.5],
#         'yellow-orange': [30, 177.5, 177.5],
#         'yellow': [39, 177.5, 177.5],
#         "yellow-green": [57, 177.5, 177.5],
#         'green': [89, 177.5, 177.5],
#         'blue-green': [128, 177.5, 177.5],
#         'blue': [150, 177.5, 177.5],
#         'blue-violet':[179, 177.5, 177.5],
#         'violet': [198, 177.5, 177.5],
#         'red-violet':[237, 177.5, 177.5]
#     }

#     neutral_dict = {
#         'white': [],
#         'black': [],
#         'gray': [],
#         'beige': []
#     }
    
#     # Find the color that h is closest to
#     # print("Hue of this pixes is :", H)

#     prevColor = 'red'
#     pixel_color = ''
#     for color in color_dict:
#         hue_val = color_dict[color][0]

#         if H < hue_val:
#             # find the closest one and return
#             prev_hue = color_dict[prevColor][0]
#             if abs(H - prev_hue) < abs(H - hue_val):
#                 pixel_color = prevColor
#             else:
#                 pixel_color = color
#             break

#         prevColor = color
    
#     if pixel_color == '':
#         # compare between red and red-violet
#         if (abs(H - 255) < abs(H - color_dict["red-violet"][0])):
#             pixel_color = "red"
#         else:
#             pixel_color = "red-violet"
    
#     if pixel_color == 'yellow-orange' and S < 100 and V > 200:
#         return 'beige'

#     # print("Determined pixel of hue", H, "to be", pixel_color)

#     return pixel_color

# def determineColor(H,S,V):
#     color_dict = {
#         'red': [0, 177.5, 177.5],
#         'red-orange': [19.4, 177.5, 177.5],
#         'orange': [38.8, 177.5, 177.5],
#         'yellow-orange': [49.4, 177.5, 177.5],
#         'yellow': [60, 177.5, 177.5],
#         "yellow-green": [90, 177.5, 177.5],
#         'green': [120, 177.5, 177.5],
#         'blue-green': [180, 177.5, 177.5],
#         'blue': [240, 177.5, 177.5],
#         'blue-violet':[256.8, 177.5, 177.5],
#         'violet': [273.6, 177.5, 177.5],
#         'red-violet':[316.8, 177.5, 177.5]
#     }

#     neutral_dict = {
#         'white': [],
#         'black': [],
#         'gray': [],
#         'beige': []
#     }
    
#     # Find the color that h is closest to
#     print("Hue of this pixes is :", H)

#     prevColor = 'red'
#     pixel_color = ''
#     for color in color_dict:
#         hue_val = color_dict[color]

#         if H < hue_val:
#             # find the closest one and return
#             prev_hue = color_dict[prevColor]
#             if abs(H - prev_hue) < abs(H - hue_val):
#                 pixel_color = prevColor
#             else:
#                 pixel_color = color
#             break

#         prevColor = color
    
#     if pixel_color == '':
#         # compare between red and red-violet
#         if (abs(H - color_dict["red"]) < abs(H - color_dict["red-violet"])):
#             pixel_color = "red"
#         else:
#             pixel_color = "red-violet"
    

#     print("Determined pixel of hue", H, "to be", pixel_color)

#     return pixel_color
        

def ColorDetectionPipe(xmin, xmax, ymin, ymax, picturePath, outputPath, clothing_item):
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
        'red':0,
        'red-orange': 0,
        'orange': 0,
        'yellow-orange': 0,
        'yellow': 0,
        'yellow-green': 0,
        'green': 0,
        'blue-green' : 0,
        'blue': 0,
        'blue-violet' : 0,
        'violet': 0,
        'red-violet' : 0,
        'white': 0,
        'black': 0,
        "gray": 0,
        'unknown': 0, 
    }


    for i in range(xmin,xmax, 1):
        for j in range(ymin,ymax, 1):
            pixel = img[j,i]
            color = DetermineColor(pixel[0],pixel[1],pixel[2])
            if not (color == "unknown"):
                if ('red' in color):
                    color_dict_scores['red'] += 1
                else:
                    color_dict_scores[color] += 1
    
    primary_color = max(color_dict_scores, key=color_dict_scores.get)
    secondary_color = sorted(color_dict_scores, key=color_dict_scores.get)[-2]
    for color in color_dict_scores:
        print(color + ": " + str(color_dict_scores[color]))
            
    print("----")

    font = cv2.FONT_HERSHEY_SIMPLEX
    outImg = cv2.imread(outputPath)
    #outImg = Image.open(outputPath)

    # print("Size:: " + str(outImg.size))
    # print("Width:: " + str(outImg.width))
    # print("Height:: " + str(outImg.height))

    # cv2.rectangle(outImg,(xmin, ymax),(xmax, ymin),(255,255,0),1)
    # cv2.putText(outImg,"primary color: " + primary_color,(xmin+10, ymax+20),font, 1.0, (0,0,0), 1, cv2.LINE_AA)

    label_str = clothing_item + " " + primary_color

    # Only returns secondary color if it is greater than 15% of primary color
    primaryScore = color_dict_scores[primary_color]
    secondaryScore = color_dict_scores[secondary_color]
    
    primary_color_return = (primary_color, primaryScore)
    secondary_color_return = (secondary_color, secondaryScore)

    if secondaryScore > (primaryScore * 0.15):
        label_str += ", " + secondary_color
        # outImg = draw_annotated_box(outImg, [(xmin,ymin,xmax,ymax)], [label_str], [(159, 43, 104)])
        drawPrettyBox(xmin, xmax, ymin, ymax, label_str, outputPath)

        cv2.destroyAllWindows()

        return [primary_color, secondary_color]
    
    # Save the cv2 img

    # outImg = draw_annotated_box(outImg, [(xmin,ymin,xmax,ymax)], [label_str], ([]))
    # outImg.save(outputPath)
    drawPrettyBox(xmin, xmax, ymin, ymax, label_str, outputPath)
    cv2.destroyAllWindows()

    return [primary_color]



    # return [primary_color_return,secondary_color_return, ("unknown", unknown_value)]


