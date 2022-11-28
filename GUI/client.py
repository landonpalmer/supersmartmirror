import requests
import cv2
import time
import requests
import geocoder
from timezonefinder import TimezoneFinder
import os

g = geocoder.ip('me')
latlng = g.latlng
lat = latlng[0]
lng = latlng[1]

obj = TimezoneFinder()
timezone = obj.timezone_at(lat=lat,lng=lng)



url = "https://trueway-geocoding.p.rapidapi.com/ReverseGeocode"

querystring = {"location":str(lat) + "," + str(lng),"language":"en"}

headers = {
	"X-RapidAPI-Key": "d339a90530msh02f7f7696c0ebc7p1f4214jsn61f8645aacf0",
	"X-RapidAPI-Host": "trueway-geocoding.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring).json()
city_name = response["results"][0]["locality"]
print("city is", city_name)




current_weather_url = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lng) + "&appid=05ddd012148db5ca45918a76ec4ac21b"
weather_forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat=" + str(lat) + "&lon=" + str(lng) + "&appid=05ddd012148db5ca45918a76ec4ac21b"
high_low_weather_url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(lng) + "&timezone=" + timezone + "&daily=temperature_2m_max,temperature_2m_min"

current_weather = requests.request("GET", current_weather_url).json()
forecast_weather = requests.request("GET", weather_forecast_url).json()
h_l_weather = requests.request("GET", high_low_weather_url).json()

temperature = int(float((current_weather['main']['temp'] - 272.15)  * (9/5) + 32))
description = current_weather['weather'][0]['description']
percent_precip = float(forecast_weather['list'][0]['pop']) * 100
high_temp = int(float(h_l_weather["daily"]["temperature_2m_max"][0]  * (9/5) + 32))
low_temp = int(float(h_l_weather["daily"]["temperature_2m_min"][0]  * (9/5) + 32))


print("It is ", temperature, "F")
print("With a high of", high_temp, "F\nand a low of", low_temp, "F")
print("There is a", percent_precip, "\ chance of precipitation")

# to open/create a new html file in the write mode
f = open('GFG.html', 'w')


testing = """testing the temp is {0}""".format(temperature)
print(testing)
# the html code which will go in the file GFG.html
html_template = """<html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Super Smart Mirror</title>
</head>
<body style="background-color: #120D31;">
    <div style="background-color: #120D31; display: grid; align-items: center; position: fixed; width: 100%; height: 80%;">
        <div style="padding: 0;">
            <div id="title-header" style="text-align: center; padding-top: 5%; padding: 0;">
                <h1 style="color: #F0D3F7;">Welcome to the Super Smart Mirror!</h1>
            </div>
            <div id="time" style="text-align: center;">
                <h2 id="clock" style="color: #F0D3F7;">6:10 PM</h2>
            </div>
            <div id="weather-div" style="text-align: center;">
                <h2 style="margin: 0; color: #F0D3F7;">""" + city_name + """</h2>
                <h3 style="margin: 0; color: #F0D3F7;">""" + description + """</h3>
                <h1 style="margin: 0; margin-top: 10px; margin-bottom: 10px; color: #F0D3F7;">""" + str(temperature) + """&deg;F</h1>
                <h5 style="margin: 0; color: #F0D3F7;">
                    <p style="margin: 0; color: #F0D3F7;">H: """ + str(high_temp) + """&deg;  L: """ + str(low_temp) + """&deg;</p>
                </h5>
                <h5 style="margin: 0; color: #F0D3F7;">Preciption: """ + str(percent_precip) + """%</h5>
            </div>
        </div>
        <div id="message-div" style="width: 50%; margin-left: auto; margin-right: auto; text-align: center;">
            <h1 style="color: #F0D3F7;">Press the button to take a picture and see if your outfit matches</h1>
        </div>
        <div style="text-align: center; position: fixed; left: 0; bottom: 0; width: 100%; margin-bottom: 3%;">
            <p style="margin: 0; color: #F0D3F7;">Cat Fact: Cats have legs.</p>
        </div>
    </div>
    <script>
        function Time() {
            var date = new Date();
            var hour = date.getHours();
            var minute = date.getMinutes();
            var second = date.getSeconds();
            
            // Variable to store AM / PM
            var period = "";

            if (hour >= 12) {
                period = "PM";
            } else {
                period = "AM";
            }

            // Converting the hour in 12-hour format
            if (hour == 0) {
                hour = 12;
            } else {
                if (hour > 12) {
                    hour = hour - 12;
                }
            }
        
            // Updating hour, minute, and second
            // if they are less than 10
            hour = update(hour);
            minute = update(minute);
            second = update(second);
            // Adding time elements to the div
            document.getElementById("clock").innerText = hour + " : " + minute + " : " + second + " " + period;
            // Set Timer to 1 sec (1000 ms)
            setTimeout(Time, 1000);
        }

        // Function to update time elements if they are less than 10
        // Append 0 before time elements if they are less than 10
        function update(t) {
            if (t < 10) {
                return "0" + t;
            }
            else {
                return t;
            }
        }

        Time();
    </script>
</body>
</html>
"""
  
# writing the code into the file
f.write(html_template)
  
# close the file
f.close()

os.system("start Chrome.exe --app=C:/Users/wjpas/OneDrive/Documents/A_Fall_2022/CSCE-489/sockets/GFG.html --start-fullscreen")



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

        img_path = "./opencv_frame.png"
        cv2.imwrite(img_path, img)
        print("{} written!".format(img_path))
        
        break

cam.release()

cv2.destroyAllWindows()


url = 'http://192.168.0.13:5000/processing'
result = requests.post(url, files={'image': open('./opencv_frame.png', 'rb')})
print(result.text)
