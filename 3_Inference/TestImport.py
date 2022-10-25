



class TestImport:
    def test():
        print("WAZZZUPP")


# def GetClothingItems(img_path):

#     os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

#     # Set up folder names for default values
#     data_folder = os.path.join(get_parent_dir(n=1), "Data")

#     image_folder = os.path.join(data_folder, "Source_Images")

#     image_test_folder = os.path.join(image_folder, "Test_Images")

#     detection_results_folder = os.path.join(image_folder, "Test_Image_Detection_Results")
#     detection_results_file = os.path.join(detection_results_folder, "Detection_Results.csv")

#     model_folder = os.path.join(data_folder, "Model_Weights")

#     model_weights = os.path.join(model_folder, "trained_weights_final.h5")
#     model_classes = os.path.join(model_folder, "data_classes.txt")

#     anchors_path = os.path.join(src_path, "keras_yolo3", "model_data", "yolo_anchors.txt")

#     FLAGS = None

#     anchors = get_anchors(anchors_path)
#     # define YOLO detector
#     yolo = YOLO(
#         **{
#             "model_path": FLAGS.model_path,
#             "anchors_path": anchors_path,
#             "classes_path": FLAGS.classes_path,
#             "score": FLAGS.score,
#             "gpu_num": FLAGS.gpu_num,
#             "model_image_size": (416, 416),
#         }
#     )
        

#     output_path = FLAGS.output
#     if not os.path.exists(output_path):
#         os.makedirs(output_path)


#     # Make a dataframe for the prediction outputs
#     out_df = pd.DataFrame(
#         columns=[
#             "image",
#             "image_path",
#             "xmin",
#             "ymin",
#             "xmax",
#             "ymax",
#             "label",
#             "confidence",
#             "x_size",
#             "y_size",
#         ]
#     )

#     # labels to draw on images
#     class_file = open(FLAGS.classes_path, "r")
#     input_labels = [line.rstrip("\n") for line in class_file.readlines()]

#     prediction, image = detect_object(
#         yolo,
#         img_path,
#         save_img=True,
#         save_img_path=FLAGS.output,
#         postfix=FLAGS.postfix,
#     )
#     y_size, x_size, _ = np.array(image).shape
#     for single_prediction in prediction:
#         out_df = out_df.append(
#             pd.DataFrame(
#                 [
#                     [
#                         os.path.basename(img_path.rstrip("\n")),
#                         img_path.rstrip("\n"),
#                     ]
#                     + single_prediction
#                     + [x_size, y_size]
#                 ],
#                 columns=[
#                     "image",
#                     "image_path",
#                     "xmin",
#                     "ymin",
#                     "xmax",
#                     "ymax",
#                     "label",
#                     "confidence",
#                     "x_size",
#                     "y_size",
#                 ],
#             )
#         )
    
#     print(out_df)