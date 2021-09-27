from flask import Flask, render_template, request, redirect, url_for ,send_from_directory
import os
from os.path import join, dirname, realpath
from flask_cors import CORS, cross_origin
import script

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
DOWNLOAD_DIRECTORY = "download"


# Root URL
@app.route('/')
@cross_origin(supports_credentials=True)
def index():
     # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')


# Get the uploaded files
@app.route("/", methods=['POST'])
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
def get_files(path):

    """Download a file."""
    return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)

@app.route('/runscript')
def dynamic_page():
    return script.your_function_in_the_module()



if (__name__ == "__main__"):
     app.run(port = 5000)