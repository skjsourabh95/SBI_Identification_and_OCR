# face detection 

import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from extract_image_from_pdf import extract_images
from retinaface import RetinaFace

# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    
    return ((left, top), (right, bottom))

def drawFaceRectangles(img,detected_faces) :
    # For each face returned use the face rectangle and draw a red box.
    print('Drawing rectangle around face... see popup for results.')
    draw = ImageDraw.Draw(img)
    for face in detected_faces:
        draw.rectangle(getRectangle(face), outline='red')
    img.show()

def extract_faces(detected_faces):
    faces = {}
    for fc in detected_faces:
        face_id = fc.face_id
        rect = fc.face_rectangle
        left = rect.left
        top = rect.top
        right = left + rect.width
        bottom = top + rect.height
        faces[face_id] = [left, top, right, bottom]
    return faces

def get_faces(image_url,config,debug=False):
    face_client = FaceClient(config["FACE_ENDPOINT"], CognitiveServicesCredentials(config["FACE_KEY"]))
    print('DETECT FACES')
    # Detect a face in an image that contains a single face
    # We use detection model 3 to get better performance.
    detected_faces = face_client.face.detect_with_url(url=image_url, detection_model='detection_03')
    faces = {}
    if debug:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        drawFaceRectangles(img,detected_faces)

    faces = extract_faces(detected_faces)
    return faces

def extract_faces_pdf(detected_faces):
    faces = {}
    for page_no,fces in detected_faces.items():
        if type(fces) == dict:
            faces[page_no] = {}
            for face_id, f in fces.items():
                faces[page_no][face_id] = {
                                            "score":f['score'], 
                                            "facial_area": [int(x) for x in f['facial_area']]
                                         } 
    return faces

def get_faces_pdf(path,debug):
    images_from_pdf = extract_images(path)
    detected_faces = {}
    for i,img_path in enumerate(images_from_pdf):
        # detected_faces[i] = DeepFace.detectFace(img_path = img_path, enforce_detection=False,detector_backend = "opencv")
        detected_faces[i] = RetinaFace.detect_faces(img_path)
    if debug:
        print(detected_faces)
    faces = extract_faces_pdf(detected_faces)
    return faces

def detect_faces(path,config,debug=False):
    if 'pdf' in path.lower():
        return get_faces_pdf(path,debug)
    else:
        return get_faces(path,config,True)