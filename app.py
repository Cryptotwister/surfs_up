# import the dependencies
from typing_extensions import runtime
from flask import Flask

# create a flask application called app
app = Flask(__name__)

# Create Flask Routes
@app.route('/')
def hello_world():
    return 'Hello world'

