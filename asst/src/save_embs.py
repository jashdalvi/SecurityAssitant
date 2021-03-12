import argparse 
from imutils import paths,resize
import cv2
import os
import pickle
import face_recognition
import pickle
import numpy as np
import dlib
from facealigner import FaceAligner

predictor = dlib.shape_predictor(os.path.join('..','data/shape_predictor_68_face_landmarks.dat'))
fa = FaceAligner(predictor, desiredFaceWidth=256)

def predict_boxes(resized_frame,faceNet):

    h,w = resized_frame.shape[:2]
    blob = cv2.dnn.blobFromImage(resized_frame, 1.0, (300, 300),(104.0, 177.0, 123.0))
    
    faceNet.setInput(blob)
	
    detections = faceNet.forward()


    boxes = []

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5 :
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX,startY,endX,endY) = box.astype('int')
            (startX,startY) = (max(0,startX), max(0,startY))
            (endX,endY) = (min(w-1,endX), min(h-1,endY))

            boxes.append((startY,endX,endY,startX))
    
    return boxes

imagepaths = paths.list_images(os.path.join("..",'Dataset'))
imagepaths_aug = paths.list_images(os.path.join("..",'Dataset_aug'))
imagepaths_aug_advanced = paths.list_images(os.path.join("..",'Dataset_aug_advanced'))

prototxtPath = os.path.join("..",os.path.join('face_detector', "deploy.prototxt"))
weightsPath = os.path.join("..",os.path.join('face_detector',"res10_300x300_ssd_iter_140000.caffemodel"))
faceNet = cv2.dnn.readNet(prototxtPath,weightsPath)

embeddings = []
labels = []
super_total = 0
for i,imagepath in enumerate(imagepaths):
    image = cv2.imread(imagepath)
    #rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    label = imagepath.split(os.path.sep)[-2]
    super_total +=1
    if super_total % 100 == 0:
       print('Processed {} images'.format(super_total)) 
    resized_frame = resize(image,width = 750)


    #boxes = face_recognition.face_locations(rgb_image,model = 'cnn')
    boxes =  predict_boxes(resized_frame,faceNet)
    gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    for box in boxes:
    # extract the ROI of the *original* face, then align the face
    # using facial landmarks
        (x, y, w, h) = (box[-1],box[0],box[1] - box[-1],box[2] - box[0])
        #rect = Rect(x, y, w, h)
        rect = dlib.rectangle(left=box[3], top=box[0], right=box[1], bottom=box[2])
        faceAligned = fa.align(resized_frame, gray, (rect))

        rgb_frame = cv2.cvtColor(faceAligned,cv2.COLOR_BGR2RGB)

        encodings = face_recognition.face_encodings(rgb_frame,[(0,rgb_frame.shape[0],rgb_frame.shape[1],0)])

        for encoding in encodings:
            embeddings.append(encoding)
            labels.append(label)

for i,imagepath in enumerate(imagepaths_aug):
    image = cv2.imread(imagepath)
    #rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    label = imagepath.split(os.path.sep)[-2]
    super_total +=1
    if super_total % 100 == 0:
       print('Processed {} images'.format(super_total)) 
    resized_frame = resize(image,width = 750)


    #boxes = face_recognition.face_locations(rgb_image,model = 'cnn')
    boxes =  predict_boxes(resized_frame,faceNet)
    gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    for box in boxes:
    # extract the ROI of the *original* face, then align the face
    # using facial landmarks
        (x, y, w, h) = (box[-1],box[0],box[1] - box[-1],box[2] - box[0])
        #rect = Rect(x,y,w,h)
        rect = dlib.rectangle(left=box[3], top=box[0], right=box[1], bottom=box[2])
        faceAligned = fa.align(resized_frame, gray, (rect))

        rgb_frame = cv2.cvtColor(faceAligned,cv2.COLOR_BGR2RGB)

        encodings = face_recognition.face_encodings(rgb_frame,[(0,rgb_frame.shape[0],rgb_frame.shape[1],0)])

        for encoding in encodings:
            embeddings.append(encoding)
            labels.append(label)

for i,imagepath in enumerate(imagepaths_aug_advanced):
    image = cv2.imread(imagepath)
    #rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    label = imagepath.split(os.path.sep)[-2]
    super_total +=1
    if super_total % 100 == 0:
       print('Processed {} images'.format(super_total)) 
    resized_frame = resize(image,width = 750)


    #boxes = face_recognition.face_locations(rgb_image,model = 'cnn')
    boxes =  predict_boxes(resized_frame,faceNet)
    gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    for box in boxes:
    # extract the ROI of the *original* face, then align the face
    # using facial landmarks
        (x, y, w, h) = (box[-1],box[0],box[1] - box[-1],box[2] - box[0])
        #rect = Rect(x,y,w,h)
        rect = dlib.rectangle(left=box[3], top=box[0], right=box[1], bottom=box[2])
        faceAligned = fa.align(resized_frame, gray, (rect))

        rgb_frame = cv2.cvtColor(faceAligned,cv2.COLOR_BGR2RGB)

        encodings = face_recognition.face_encodings(rgb_frame,[(0,rgb_frame.shape[0],rgb_frame.shape[1],0)])

        for encoding in encodings:
            embeddings.append(encoding)
            labels.append(label)

data = {'embeddings': embeddings,'labels':labels}

emb_path = os.path.join("..",'data/data.pickle')
if os.path.exists(emb_path):
    os.remove(emb_path)

with open(emb_path,'wb') as f:
    pickle.dump(data,f)





