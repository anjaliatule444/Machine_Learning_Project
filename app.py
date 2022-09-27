from flask import Flask,request,app
from housing.logger import logging
import sys
from housing.exception import HousingException

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    try:
        raise Exception("Exception Testing")
    except Exception as e:
        housing=HousingException(e,sys)
        logging.info(housing.error_message)
    logging.info("logging Module testing")
    return "Hello Varad"

if __name__ == "__main__":
    app.run(debug=True)