from flask import request
from flask_json import json_response
from tools.logging import logger
from tools.model import imagePredicition
import os
from werkzeug.utils import secure_filename # prevent SQL injection

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp'])
TEMP_FOLDER = './images/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# should delete the temp image, untested
def delete_temp_file(tempFile):
    if os.path.exists(tempFile):
        os.remove(tempFile)
    else:
        logger.debug("The file does not exist")


def handle_request():
    logger.debug("Open_Upload called")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return json_response(status = 412, message = "No files submitted")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return json_response(status = 415, message = "File type not found.")
        if not allowed_file(file.filename):
            return json_response(status = 415, message = "File type not supported.")
        if file and allowed_file(file.filename):
            logger.debug("File accepted and being processed")
            filename = secure_filename(file.filename)
            logger.debug("Trying to save file")
            #save the file to temp
            file.save(os.path.join(TEMP_FOLDER, filename))
            tempFile = TEMP_FOLDER + filename
            #send the image to the prediction
            logger.debug("Sending image to model")
            prediction = imagePredicition(tempFile)
            #delete the file uploaded for testing
            logger.debug("Deleting image used")
            delete_temp_file()
            #return the prediction to user
            logger.debug("Sending back response")
            return json_response(status = 200, message = prediction)
