import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IP
client.connect(('192.168.0.19', 1025)) 

file = open('IMG_0336.JPG', 'rb')
image_data = file.read(2048)

while image_data:
    client.send(image_data)
    image_data = file.read(2048)

file.close()
client.close()