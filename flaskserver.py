import os
import sys
import cv2
import time


def get_parent_dir(n=1):
    """returns the n-th parent dicrectory of the current
    working directory"""
    current_path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(n):
        current_path = os.path.dirname(current_path)
    return current_path


src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "2_Training", "src")
utils_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Utils")
color_detection_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ColorDetection")
color_wheel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ColorMatching")

print(src_path)

sys.path.append(src_path)
sys.path.append(utils_path)
sys.path.append(color_detection_path)
sys.path.append(color_wheel_path)

import argparse
from keras_yolo3.yolo import YOLO, detect_video, detect_webcam
from PIL import Image
from timeit import default_timer as timer
from utils import load_extractor_model, load_features, parse_input, detect_object
import test
import utils
import pandas as pd
import numpy as np
from Get_File_Paths import GetFileList
import random
from Train_Utils import get_anchors
from ColorDetectionPipe import ColorDetectionPipe
from ColorWheel import ColorWheel

from flask import Flask, render_template
app = Flask(__name__)


def getClothingItems(img_path):
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

    # Set up folder names for default values
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data")

    image_folder = os.path.join(data_folder, "Source_Images")

    image_test_folder = os.path.join(image_folder, "Test_Images")

    detection_results_folder = os.path.join(image_folder, "Test_Image_Detection_Results")
    detection_results_file = os.path.join(detection_results_folder, "Detection_Results.csv")

    model_folder = os.path.join(data_folder, "Model_Weights")

    model_weights = os.path.join(model_folder, "trained_weights_final.h5")
    model_classes = os.path.join(model_folder, "data_classes.txt")

    anchors_path = os.path.join(src_path, "keras_yolo3", "model_data", "yolo_anchors.txt")

    anchors = get_anchors(anchors_path)
    # define YOLO detector
    yolo = YOLO(
        **{
            "model_path": model_weights,
            "anchors_path": anchors_path,
            "classes_path": model_classes,
            "score": 0.25,
            "gpu_num": 1,
            "model_image_size": (416, 416),
        }
    )
        

    output_path = detection_results_folder
    if not os.path.exists(output_path):
        os.makedirs(output_path)


    # Make a dataframe for the prediction outputs
    out_df = pd.DataFrame(
        columns=[
            "image",
            "image_path",
            "xmin",
            "ymin",
            "xmax",
            "ymax",
            "label",
            "confidence",
            "x_size",
            "y_size",
        ]
    )

    # labels to draw on images
    class_file = open(model_classes, "r")
    input_labels = [line.rstrip("\n") for line in class_file.readlines()]

    prediction, image = detect_object(
        yolo,
        img_path,
        save_img=True,
        save_img_path=detection_results_folder,
        postfix="_clothing",
    )
    y_size, x_size, _ = np.array(image).shape
    for single_prediction in prediction:

        print("single prediction")
        print(single_prediction)

        out_df = out_df.append(
            pd.DataFrame(
                [
                    [
                        os.path.basename(img_path.rstrip("\n")),
                        img_path.rstrip("\n"),
                    ]
                    + single_prediction
                    + [x_size, y_size]
                    + [input_labels[single_prediction[4]]]
                ],
                columns=[
                    "image",
                    "image_path",
                    "xmin",
                    "ymin",
                    "xmax",
                    "ymax",
                    "label_index",
                    "confidence",
                    "x_size",
                    "y_size",
                    "label",
                ],
            )
        )
    
    yolo.close_session()
    
    return out_df

def captureAnalyzeClothing():
    ####### Test this on mac - WSL doesn't have write drivers or something #########
    img_path = ""
    if (len(sys.argv) <= 1):
        TIMER = 5

        # initialize the camera
        cam = cv2.VideoCapture(0)

        cv2.namedWindow("Camera")

        while True:

            # Display the current frame
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("Camera", frame)

            # check for key to be pressed
            k = cv2.waitKey(1)
            if k%256 == 32:
                # SPACE pressed start countdown timer

                prev = time.time()
                
                while TIMER >= 0:
                    ret, frame = cam.read()

                    # Display the countdown on the frame
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, str(TIMER), (200, 250), font, 7, 
                        (0, 255, 255), 4, cv2.LINE_AA)
                    cv2.imshow('Camera', frame)
                    cv2.waitKey(125)

                    # get current time
                    curr = time.time()

                    if curr-prev >= 1:
                        prev = curr
                        TIMER = TIMER - 1
                    
                
                ret, img = cam.read()
                cv2.imshow('Camera', img)

                cv2.waitKey(2000)

                img_path = "./Data/Source_Images/Test_Image_Detection_Results/opencv_frame.jpg"
                cv2.imwrite(img_path, img)
                print("{} written!".format(img_path))
                
                break

        cam.release()

        cv2.destroyAllWindows()
    else:
        img_path = sys.argv[1]

    #--------- Clothing Item Detection -------------
    clothingItemsDF = getClothingItems(img_path)
    out_path = "./Data/Source_Images/Test_Image_Detection_Results/opencv_frame_colors.jpg"

    colorList = []
    colorSet = set()

    # Set the initial image
    img = cv2.imread(img_path)
    cv2.imwrite(out_path, img)

    for index, row in clothingItemsDF.iterrows():
        xmin = row["xmin"]
        xmax = row["xmax"]
        ymin = row["ymin"]
        ymax = row["ymax"]

        print("Row is", row)
        
        ######### ColorDetectionPipe throws an error -- also should return list of colors (id doesn't right now) #####

        itemColorsSet = ColorDetectionPipe(xmin, xmax, ymin, ymax, img_path, out_path)
        #colorDetection returns an array of [(primary_color, score),(secondary_color, score), (unknown, score)]
        #I want to compare the amount of unknown pixels to the primary and secondary to see if it would be a good idea to filter not great data
        #for now i think ill just place the item colors as primary and secondary
        # itemColors = [itemColorsSet[0][0], itemColorsSet[1][0]]
        itemColors = itemColorsSet
        # colorList.extend(itemColors)
        # itemColors = ["red", "green", "blue"]
        for color in itemColors:
            colorSet.add(color)
        print(row["label"], "determined to be", itemColors)


    # clothingItemsDF['Colors'] = colorList

    wheel = ["red", "red-orange", "orange", "yellow-orange", "yellow", "yellow-green", "green", "blue-green", "blue", "blue-violet", "violet", "red-violet"]
    neutralColors = ["black", "white", "gray", "beige"]

    cw = ColorWheel(wheel)

    colorList.clear()
    colorList = list(colorSet)
    tempSize = len(colorList)

    hadNeutral = tempSize == len(colorList)

    print("Color list is", colorList)

    # Remove all neutral colors from colorlist
    colorList = list(set(colorList).difference(neutralColors))

    print("Color List is now", colorList)

    if len(colorList) <= 1 and hadNeutral:
        print("Colors Match!!")
        return "Colors match"
    elif (len(colorList) == 2):
        if (cw.do2ColorsMatch(colorList[0], colorList[1])):
            print("Colors Match!!")
            return "Colors match"
        else:
            print("Colors don't match :(")
            print("Try theese color combinatios:")

            print("Color combination(s) for", colorList)
            for colors in cw.thirdColorSuggestion(colorList[0], colorList[1]):
                print(colors)

            print("Color combination(s) for", colorList[0])
            for colors in cw.secondColorSuggestion(colorList[0]):
                print(colors)
            
            print("Color combination(s) for", colorList[1])
            for colors in cw.secondColorSuggestion(colorList[1]):
                print(colors)

            return "Colors do not match"
    elif (len(colorList) == 3):
        if (cw.do3ColorsMatch(colorList[0], colorList[1], colorList[2])):
            print("Colors Match!!")
            return "Colors match"
        else:
            print("Colors don't match :(")
            print("Try theese color combinatios:")

            print("Color combination(s) for (" + colorList[0] + ", " + colorList[1] + ")")
            for colors in cw.thirdColorSuggestion(colorList[0], colorList[1]):
                print(colors)

            print("Color combination(s) for(" + colorList[0] + ", " + colorList[2] + ")")
            for colors in cw.thirdColorSuggestion(colorList[0], colorList[2]):
                print(colors)
            
            print("Color combination(s) for(" + colorList[1] + ", " + colorList[2] + ")")
            for colors in cw.thirdColorSuggestion(colorList[1], colorList[2]):
                print(colors)
            return "Colors don't match"

@app.route('/')
def index():
    clothingMatchString = captureAnalyzeClothing()
    return clothingMatchString

if __name__ == '__main__':
     app.run(debug=True, port=8001)