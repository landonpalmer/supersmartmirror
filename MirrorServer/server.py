from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def test():
    return { 'test' : "Gus sends his regards" }   
if __name__ == '__main__':
    app.run(debug=True)