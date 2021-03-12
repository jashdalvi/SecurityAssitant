#python create_dataset.py -- label Jash
import cv2
import argparse
import os 
import imutils
import numpy as np
import time


ap = argparse.ArgumentParser()
ap.add_argument('-l','--label',help = "name of the person",required = True)
ap.add_argument('-i','--input',help="any other input video",default = None)

args = vars(ap.parse_args())
labels_path = os.path.join("..",os.path.join('Dataset',args['label']))

if not os.path.exists(labels_path):
    os.mkdir(labels_path)

cap = cv2.VideoCapture(args['input'] if args['input'] else 0)
image_num = 0
starting_time = time.time()
while True:

    (grabbed,frame) = cap.read()

    if not grabbed:
        break
    
    save_frame = frame.copy()

    frame = imutils.resize(frame, width = 700)

    cv2.putText(frame,"Total Images Stored: {}".format(str(image_num)),(10,25),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255), 2)
    cv2.imshow('Frame',frame)
    key = cv2.waitKey(1) & 0xFF
    


    if key == ord('k'):
        image_num += 1
        label = '{}{}.png'.format(args['label'],str(image_num).zfill(2))
        path = os.path.join(labels_path,label)
        cv2.imwrite(path,save_frame)

    elif key == ord('q'):
        break

    ending_time = time.time()
cap.release()
cv2.destroyAllWindows()

    







