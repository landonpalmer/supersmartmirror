import os
import sys
import cv2


def get_parent_dir(n=1):
    """returns the n-th parent dicrectory of the current
    working directory"""
    current_path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(n):
        current_path = os.path.dirname(current_path)
    return current_path


src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "2_Training", "src")
utils_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Utils")

print(src_path)

sys.path.append(src_path)
sys.path.append(utils_path)

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
        postfix="_out",
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
                ],
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
                ],
            )
        )
    
    yolo.close_session()
    
    return out_df


####### Test this on mac - WSL doesn't have write drivers or something #########

# initialize the camera
# cam = cv2.VideoCapture(0)   # 0 -> index of camera
# s, img = cam.read()
# if s:    # frame captured without any errors
#     cv2.namedWindow("cam-test",cv2.CV_WINDOW_AUTOSIZE)
#     cv2.imshow("cam-test",img)
#     cv2.waitKey(0)
#     cv2.destroyWindow("cam-test")
#     cv2.imwrite("filename.jpg",img) # save img

img_path = sys.argv[1]

clothingItemsDF = getClothingItems(img_path)

