import socket
import cv2
import time

def camera():
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Camera")
    TIMER = 5
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
            img_path = "./cvFrame.jpg"
            cv2.imwrite(img_path, img)
            time.sleep(1)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IP
            client.connect(('192.168.0.19', 1025)) 
            file = open('cvFrame.jpg', 'rb')
            image_data = file.read(2048)

            while image_data:
                client.send(image_data)
                image_data = file.read(2048)

            file.close()
            client.close()
            break
    cv2.destroyAllWindows()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IP
client.connect(('192.168.0.19', 1025)) 

file = open('IMG_0336.JPG', 'rb')
image_data = file.read(2048)

while image_data:
    client.send(image_data)
    image_data = file.read(2048)

file.close()
client.close()