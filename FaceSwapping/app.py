"""
    Author: Mukesh Kumar Thakur
    Github: CaptaiN785
    Topics: Face Swapping API

"""

from flask import Flask, request, redirect, send_file, jsonify, render_template, url_for
from insightface.app import FaceAnalysis
import insightface
import cv2
import matplotlib.pyplot as plt
import os
import requests

app = Flask(__name__)

model_name = "inswapper_128.onnx"
model_link = "https://firebasestorage.googleapis.com/v0/b/faceswapping-48f93.appspot.com/o/inswapper_128.onnx?alt=media&token=674c0931-c606-4014-b938-836c35a8f3f9"

if not os.path.exists(model_name):
    print("Downloading model...")
    data = requests.get(model_link)
    with open(model_name, "wb") as file:
        file.write(data.content)
    print("Model downloaded!")
else:
    print("Model already downloaded!")

## Defining the face detector
detector = FaceAnalysis(name='buffalo_l')
detector.prepare(ctx_id=0, det_size=(640, 640))


## Loading the model.
swapper = insightface.model_zoo.get_model(model_name,
                                          download=False,
                                          download_zip=False)

def swap_faces(target, source, show_only=False):
    # Creating a result image copy
    res = target.copy()

    # Finding single image in source_face
    source_face = detector.get(source)[0]
    assert source_face is not None

    # Find all faces to replace in target images
    target_faces = detector.get(target)
    for face in target_faces:
        res = swapper.get(res, face, source_face, paste_back=True)

    # If function is called just to show image
    # Otherwise return image
    if show_only:
        plt.imshow(res[:,:, ::-1])
        plt.axis("off")
        plt.show
    else:
        return res

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/swap', methods=['POST', 'GET'])
def swap():
    # If post is sent then swap the face.
    if request.method == "POST":
        try:
            source_file = request.files['source']
            target_file = request.files['target']

            source_file.save("static/source.jpg")
            target_file.save("static/target.jpg")
            
            source = cv2.imread("static/source.jpg")
            target = cv2.imread("static/target.jpg")

            if source is None:
                raise FileNotFoundError("Source not found")
            if target is None:
                raise FileNotFoundError("Target not found")
            
            res = swap_faces(target, source)
            cv2.imwrite("static/result.jpg", res)
            return jsonify({
                "url" : 'result.jpg',
                "success":"true"
            })
        except Exception as e:
            print(e)
            return jsonify({
                "success":"false",
                "status":"400",
                "message":"Unable to find source or target file."
            })
    return jsonify({
                "status":"200",
                "message":"Welcome to get method of /swap"
            })

if __name__ == '__main__':
    app.run(debug=True)