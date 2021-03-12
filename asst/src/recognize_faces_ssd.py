import pickle
import argparse
import imutils
import face_recognition
import numpy as np 
import cv2
import os
import time
from collections import Counter
import dlib
from asst.src.facealigner import FaceAligner

predictor = dlib.shape_predictor('/home/jash/Desktop/JashWork/asst/asst/data/shape_predictor_68_face_landmarks.dat')
fa = FaceAligner(predictor, desiredFaceWidth=256)

head_model_path = '/home/jash/Desktop/JashWork/asst/asst/data/head_model.sav'
scaling_path = '/home/jash/Desktop/JashWork/asst/asst/data/scaling.pkl'
labelencoder_path = '/home/jash/Desktop/JashWork/asst/asst/data/labelencoder.pkl'

#labels = os.listdir('Dataset')
with open(scaling_path, 'rb') as f:
    scalar_all = pickle.load(f)

with open(labelencoder_path,'rb') as flabel:
    le = pickle.load(flabel)

def predict_faces_and_names(resized_frame,faceNet,model):

    h,w = resized_frame.shape[:2]
    blob = cv2.dnn.blobFromImage(resized_frame, 1.0, (300, 300),(104.0, 177.0, 123.0))
    
    faceNet.setInput(blob)
	
    detections = faceNet.forward()


    boxes = []
    names = []

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5 :
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX,startY,endX,endY) = box.astype('int')
            (startX,startY) = (max(0,startX), max(0,startY))
            (endX,endY) = (min(w-1,endX), min(h-1,endY))

            boxes.append((startY,endX,endY,startX))
    gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    #rgb_frame = cv2.cvtColor(resized_frame,cv2.COLOR_BGR2RGB)
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
            index = model.predict(scalar_all.transform([encoding]))[0]
            names.append(list(le.inverse_transform([index]))[0])

    return boxes,names








#ap = argparse.ArgumentParser()
#ap.add_argument('-i','--input',help="any other input video",default = None)
#ap.add_argument('-f','--face',default = 'face_detector',help = 'path to the face detector model')
#args = vars(ap.parse_args())

prototxtPath = '/home/jash/Desktop/JashWork/asst/asst/face_detector/deploy.prototxt'
weightsPath = '/home/jash/Desktop/JashWork/asst/asst/face_detector/res10_300x300_ssd_iter_140000.caffemodel'
faceNet = cv2.dnn.readNet(prototxtPath,weightsPath)

USE_GPU=False

if USE_GPU:

	
	print("[INFO] setting preferable backend and target to CUDA...")
	faceNet.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
	faceNet.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
 
with open(head_model_path,'rb') as f:
    model = pickle.load(f)

#cap = cv2.VideoCapture(0)
#width = int(cap.get(3))
#height =int(cap.get(4))
#out = cv2.VideoWriter(os.path.join("..",'output/facecam1.mp4'),cv2.VideoWriter_fourcc('M','J','P','G'),6,(width,height))
#labels = os.listdir('Dataset')
#starting_time = time.time()
frame_id = 0
names_display = []
class FaceDetect():
    def __init__(self):
        self.frame_id = 0
        self.names_display = []
        self.name_to_display = None
    

    def camera_init(self):
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):

        (grabbed,frame) = self.cap.read()
        starting_time = time.time()
        self.frame_id += 1
        #if not grabbed:
        #    break

    #   rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        resized_frame = imutils.resize(frame,width = 750)
        r = frame.shape[1]/float(resized_frame.shape[1])

        

        boxes,names = predict_faces_and_names(resized_frame,faceNet,model)

    #    boxes = face_recognition.face_locations(rgb_frame,model = 'hog')

    #    encodings = face_recognition.face_encodings(rgb_frame,boxes)

    #    names = []
    #    for encoding in encodings:
    #        index = model.predict([encoding])[0]
    #        names.append(labels[index])

        for ((top,right,bottom,left),name) in zip(boxes,names):
            top = int(top*r)
            right = int(right*r)
            bottom = int(bottom*r)
            left = int(left*r)
            cv2.rectangle(frame,(left,top),(right,bottom),(0,255,0),2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame,name,(left,y),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,255,0),2)
            self.names_display.append(name)


        elapsed_time = time.time() - starting_time
        fps = 1 / elapsed_time
        #cv2.putText(frame,"FPS: {}".format(str(round(fps,3))),(10,25),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255),2)

        #cv2.imshow('Frame',frame)
        #out.write(frame)
        #key = cv2.waitKey(1) & 0xFF

        #if key == ord('q'):
        #   break
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def destroy(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def get_name(self):
        names_dict = dict(Counter(self.names_display))
        max_display = 0
        for key,value in names_dict.items():
            if value > max_display:
                max_display = value
                self.name_to_display = key

        return self.name_to_display


#display_names=dict(Counter(names_display))
#max_display = 0
#name_to_display = None
#for key,value in display_names.items():
#    if value > max_display:
#        max_display = value
#        name_to_display = key

#print(display_names)
#print(name_to_display)
#out.release()
#cap.release() 
#cv2.destroyAllWindows()