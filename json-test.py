# import json
# import base64


# items_path = "./Data/Source_Images/Test_Image_Detection_Results/opencv_frame_clothing.jpg"

# data = {}
# with open(items_path, mode='rb') as file:
#     img = file.read()

# data['img'] = base64.encodebytes(img)

# print(json.dumps(data))


from base64 import b64encode
from json import dumps

ENCODING = 'utf-8'
IMAGE_NAME = './Data/Source_Images/Test_Image_Detection_Results/opencv_frame_clothing.jpg'
JSON_NAME = 'output.json'

# first: reading the binary stuff
# note the 'rb' flag
# result: bytes
with open(IMAGE_NAME, 'rb') as open_file:
    byte_content = open_file.read()

# second: base64 encode read data
# result: bytes (again)
base64_bytes = b64encode(byte_content)

# third: decode these bytes to text
# result: string (in utf-8)
base64_string = base64_bytes.decode(ENCODING)

# optional: doing stuff with the data
# result here: some dict
raw_data = {IMAGE_NAME: base64_string}

# now: encoding the data to json
# result: string
json_data = dumps(raw_data, indent=2)

# finally: writing the json string to disk
# note the 'w' flag, no 'b' needed as we deal with text here
with open(JSON_NAME, 'w') as another_open_file:
    another_open_file.write(json_data)