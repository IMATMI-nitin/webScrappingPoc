import time
from flask import Flask, render_template, request, redirect, url_for ,send_from_directory, make_response
import os
from os.path import join, dirname, realpath
from flask.wrappers import JSONMixin
from flask_cors import CORS, cross_origin
#import script
import base64
import io

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
DOWNLOAD_DIRECTORY = "download"


# Root URL
@app.route('/')
def index():
     # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
          # save the file
      return redirect(url_for('index'))

@app.route('/get-files/<path:path>',methods = ['GET','POST'])
def get_files(path):

    """Download a file."""
    return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)

def scriptLog():
    return "Script executed successfully"

#@app.route('/runscript/<int:no>',methods = ['GET','POST'])
#def dynamic_page(no):
#    detes = script.all_search(no)
    #script.all_search(1)
#    response = make_response(scriptLog(), 200)
#    response.mimetype = "text/plain"
#    return response
