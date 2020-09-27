from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/other')
def other():
    return render_template('other.html')
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')