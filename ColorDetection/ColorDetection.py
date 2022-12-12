import cv2
import cython
def CompareBounds(H, S, V, upper_bound, lower_bound):
    if H <= upper_bound[0] and H >= lower_bound[0]:
            if S <= upper_bound[1] and S >= lower_bound[1]:
                if V <= upper_bound[2] and V >= lower_bound[2]:
                    return True
    return False

def DetermineColor(H, S, V):
    # color_dict_HSV = {'black': [[180, 255, 30], [0, 0, 0]],
    #           'white': [[180, 18, 255], [0, 0, 231]],
    #           'red1': [[180, 255, 255], [159, 50, 70]],
    #           'red2': [[9, 255, 255], [0, 50, 70]],
    #           'green': [[89, 255, 255], [36, 50, 70]],
    #           'blue': [[128, 255, 255], [90, 50, 70]],
    #           'yellow': [[35, 255, 255], [25, 50, 70]],
    #           'purple': [[158, 255, 255], [129, 50, 70]],
    #           'orange': [[24, 255, 255], [5, 143, 0]],
    #           'gray': [[180, 18, 230], [0, 0, 40]],
    #           'beige': [[23,255,227], [12,44,30]]
    #           }
    # if (V <= 5):
    #     return "black"
    # if (V >= 250):
    #     return "white"
    color_dict_HSV = {
        'red1': [[3,255,255],[0,132,82]],
        'red-orange': [[16,255,255],[4,59,0]],
        'orange': [[22,255,255],[17,68,0]],
        'yellow-orange': [[27,255,255],[23,56,0]],
        'yellow': [[36,255,255],[28,44,29]],
        'yellow-green' : [[56,255,255],[37,44,29]],
        'green': [[81,255,255],[57,44,29]],
        'blue-green' : [[100,255,255],[82,44,29]],
        'blue' : [[127,255,255],[101,41,29]],
        'blue-violet' : [[136, 255,255],[128, 15, 36]],
        'violet': [[154,255,255],[137,15,36]],
        'red-violet': [[162,255,255],[155,7,31]],
        'red2' : [[179,255,255],[163,38,0]],
    }
    for color in color_dict_HSV:
        upper_bound = color_dict_HSV[color][0]
        lower_bound = color_dict_HSV[color][1]
        if (CompareBounds(H, S, V, upper_bound, lower_bound)):
            if (color == "red1") or (color == "red2"):
                return "red"
            if color == "yellow-green":
                return "yellow"
            return color
    return "unknown"

def mouseclick(event, x, y, flags, param):
    global img, temp
    if event == cv2.EVENT_LBUTTONDOWN:
        xmin = x-250
        xmax = x+250
        ymin = y-250
        ymax = y+250
        img = temp
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img = cv2.rectangle(img,(xmin, ymax),(xmax, ymin),(255,255,0),1)
        color_dict_scores = {'black': 0,
              'white': 0,
              'red': 0,
              'green': 0,
              'blue': 0,
              'yellow': 0,
              'purple': 0,
              'orange': 0,
              'gray': 0,
              'unknown': 0,
              'beige': 0}
        for i in range(xmin+1,xmax-1, 3):
            for j in range(ymin+1,ymax-1, 3):
                pixel = img[i,j]
                color = DetermineColor(pixel[0],pixel[1],pixel[2])
                color_dict_scores[color] += 1
        primary_color = ""
        secondary_color = ""
        maxColor = 0
        for color in color_dict_scores:
            if color == "unknown":
                continue
            print(color+ ": " + str(color_dict_scores[color]))
            if color_dict_scores[color] > maxColor:
                secondary_color = primary_color
                primary_color = color
                maxColor = color_dict_scores[color]
            elif secondary_color == "" and color_dict_scores[color] > 0:
                secondary_color = color
        print("----")
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,"primary color: " + primary_color,(xmin+10, ymax+20),font, 1.0, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(img,"secondary_color: " + secondary_color,(xmin+10, ymax+40),font, 1.0, (0,0,0), 1, cv2.LINE_AA)
        cv2.imshow("image",img)
name_of_file= "beige_pants.jpeg"
img = cv2.imread(name_of_file)
temp = img.copy()
cv2.imshow('image',img)
cv2.setMouseCallback('image', mouseclick)
cv2.waitKey(0)
cv2.destroyAllWindows()


