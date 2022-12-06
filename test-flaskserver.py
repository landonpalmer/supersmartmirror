# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template
from clothing_detection import ColorDetection

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with index function.
def index():
    # threading.Thread(target=getClothingData()).start()
    fetched_cat_fact=cd.getClothingData()
    return render_template("index.html", cat_fact=fetched_cat_fact)
 

# main driver function
if __name__ == '__main__':
    cd = ColorDetection(0)
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(port=8001)

