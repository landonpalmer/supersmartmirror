import cv2
import numpy as np


def DetermineColor(H,S,V):

    # check for black
    if V < 20:
        return 'black'
    
    # check for white
    if V > 230:
        return 'white'
    
    # check for gray
    if S < 50:
        return 'gray'
    

    color_dict = {
        'red': [0, 177.5, 177.5],
        'red-orange': [11, 177.5, 177.5],
        'orange': [19, 177.5, 177.5],
        'yellow-orange': [30, 177.5, 177.5],
        'yellow': [39, 177.5, 177.5],
        "yellow-green": [57, 177.5, 177.5],
        'green': [89, 177.5, 177.5],
        'blue-green': [128, 177.5, 177.5],
        'blue': [150, 177.5, 177.5],
        'blue-violet':[179, 177.5, 177.5],
        'violet': [198, 177.5, 177.5],
        'red-violet':[237, 177.5, 177.5]
    }

    neutral_dict = {
        'white': [],
        'black': [],
        'gray': [],
        'beige': []
    }
    
    # Find the color that h is closest to
    print("Hue of this pixes is :", H)

    prevColor = 'red'
    pixel_color = ''
    for color in color_dict:
        hue_val = color_dict[color][0]

        if H < hue_val:
            # find the closest one and return
            prev_hue = color_dict[prevColor][0]
            if abs(H - prev_hue) < abs(H - hue_val):
                pixel_color = prevColor
            else:
                pixel_color = color
            break

        prevColor = color
    
    if pixel_color == '':
        # compare between red and red-violet
        if (abs(H - 255) < abs(H - color_dict["red-violet"][0])):
            pixel_color = "red"
        else:
            pixel_color = "red-violet"
    
    if pixel_color == 'yellow-orange' and S < 100 and V > 200:
        return 'beige'

    print("Determined pixel of hue", H, "to be", pixel_color)

    return pixel_color


picturePath = "test_pic.png"


color_dict_scores = {
    'red':0,
    'red-orange': 0,
    'orange': 0,
    'yellow-orange': 0,
    'yellow': 0,
    "yellow-green": 0,
    'green': 0,
    'blue-green': 0,
    'blue': 0,
    'blue-violet':0,
    'violet': 0,
    'red-violet':0,
    'black':0,
    'white':0,
    'beige':0,
    'gray':0
}

xmin = 50
ymin = 50
xmax = 75
ymax = 75

img = cv2.imread(picturePath) 
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)   

for i in range(xmin,xmax, 1):
        for j in range(ymin,ymax, 1):
            normal_pixel = img[j,i]
            print("normal pixel color is", normal_pixel)

            pixel = hsv_img[j,i]

            print("HSV value of the pixel is:", pixel)
            color = DetermineColor(pixel[0],pixel[1],pixel[2])
            color_dict_scores[color] += 1



hsv_img = cv2.rectangle(hsv_img,(xmin, ymax),(xmax, ymin),(255,255,0),1)

print(color_dict_scores)

cv2.imwrite("test-out.png", hsv_img)

# red_rgb = [255,0,0]
# red_orange = [255, 63, 0]
# orange = [240, 133, 45]
# yellow_orange = [242, 175, 19]
# yellow = [236, 216, 3]
# yellow_green = [154, 205, 50]
# green = [0,255,0]
# blue_green = [0, 128, 128]
# blue = [0,0,255]
# blue_violet = [37, 24, 88]
# violet = [154, 90, 191]



# colorMatrix = [
#     [255,0,0],
#     [255,63,0],
#     [240, 133, 45],
#     [242, 175, 19],
#     [236, 216, 3],
#     [154, 205, 50],
#     [0,255,0],
#     [0, 128, 128],
#     [0,0,255],
#     [37, 24, 88],
#     [154, 90, 191],
#     [130, 15, 65]
# ]



# for color in colorMatrix:
# hsv_val = cv2.cvtColor(np.uint8([[[16, 119, 26]]]), cv2.COLOR_RGB2HSV_FULL)
# print("hsv value is", hsv_val)


# print("hsv red is", hsv_red)



