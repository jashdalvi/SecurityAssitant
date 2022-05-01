#python create_dataset.py -- label Jash
import cv2
import argparse
import os 
import imutils
import numpy as np
import time
# import keyboard
from PIL import Image
# from pynput.keyboard import Controller, Key



# ap = argparse.ArgumentParser()
# ap.add_argument('-l','--label',help = "name of the person",required = True)
# ap.add_argument('-i','--input',help="any other input video",default = None)

# args = vars(ap.parse_args())
# labels_path = os.path.join("..",os.path.join('Dataset',args['label']))

# if not os.path.exists(labels_path):
#     os.mkdir(labels_path)

# cap = cv2.VideoCapture(args['input'] if args['input'] else 0)
# image_num = 0
# starting_time = time.time()
# while True:

#     (grabbed,frame) = cap.read()

#     if not grabbed:
#         break
    
#     save_frame = frame.copy()

#     frame = imutils.resize(frame, width = 700)

#     cv2.putText(frame,"Total Images Stored: {}".format(str(image_num)),(10,25),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255), 2)
#     cv2.imshow('Frame',frame)
#     key = cv2.waitKey(1) & 0xFF
    


#     if key == ord('k'):
#         image_num += 1
#         label = '{}{}.png'.format(args['label'],str(image_num).zfill(2))
#         path = os.path.join(labels_path,label)
#         cv2.imwrite(path,save_frame)

#     elif key == ord('q'):
#         break

#     ending_time = time.time()
# cap.release()
# cv2.destroyAllWindows()

class CreateDataset:
    def __init__(self):
        self.label = None
        self.image_num = 0
        self.frame_num = 1
        
        
    def camera_init(self):
        self.cap = cv2.VideoCapture(0)

    def send_label(self,label):
        self.label = label
        self.labels_path = "/home/jash/Desktop/JashWork/asst21/asst/Dataset/" + self.label
        

        if not os.path.exists(self.labels_path):
            os.mkdir(self.labels_path)

    def get_frame(self):
        grabbed,frame = self.cap.read()

        if not grabbed:
            self.destroy()
        
        save_frame = frame.copy()

        frame = imutils.resize(frame, width = 700)

        cv2.putText(frame,"Total Images Stored: {}".format(str(self.image_num)),(10,25),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255),2)
        #key = cv2.waitKey(1) & 0xFF
          # used try so that if user pressed other than the given key error will not be shown
        # if keyboard.is_pressed('k'):  # if key 'q' is pressed 
        #     self.image_num += 1
        #     print("key_pressed")
        #     label = '{}{}.png'.format(self.label,str(image_num).zfill(2))
        #     path = self.labels_path + '/' + label
        #     cv2.imwrite(path,save_frame)
        # else:
        #     print(not keyboard.is_pressed('k'))


        
        

        # key = cv2.waitKey(1)
        # print(key)
        if self.frame_num % 50 == 0:
            self.image_num += 1
            print("captured")
            label = '{}{}.png'.format(self.label,str(self.image_num).zfill(2))
            path = self.labels_path + '/' + label
            cv2.imwrite(path,save_frame)
        # j = Image.fromarray(save_frame[:,:,::-1])
        # j.save(path)
        self.frame_num += 1

        if self.image_num > 20:
            self.label = None
            self.image_num = 0
            self.frame_num = 1
            self.destroy()

        

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def destroy(self):
        self.cap.release()
        cv2.destroyAllWindows()






    







