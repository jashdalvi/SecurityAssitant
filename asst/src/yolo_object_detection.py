import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import cv2
import numpy as np
import random
import imutils
from imutils.perspective import four_point_transform
from tensorflow.keras.models import load_model
from collections import Counter
import time

# Load Yolo
yolo_weights = "/home/jash/Desktop/JashWork/asst/asst/data/yolov3_training_last.weights"
yolo_config = "/home/jash/Desktop/JashWork/asst/asst/data/yolov3_testing.cfg"
net = cv2.dnn.readNet(yolo_weights,yolo_config)

USE_GPU=False

if USE_GPU:

	
	print("[INFO] setting preferable backend and target to CUDA...")
	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Name custom object
classes = ["digit"]

head_model = load_model("/home/jash/Desktop/JashWork/asst/asst/data/digitnet2")

# Images path
# images_path = glob.glob(r"D:\Pysource\Youtube\2020\105) Train Yolo google cloud\dataset\*.jpg")
# images_path = ['21.png','25.png','703.png','708.png']



layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

starting_time = time.time()

class Temperature:
    def __init__(self):
        self.frame_id = 0
        self.temperatures = []
        self.best_temp = None

    def camera_init(self):
        self.cap = cv2.VideoCapture(0)


    def get_frame(self):
        ret,img = self.cap.read()
        #img = cv2.imread(img_path)
        #img = cv2.resize(frame, None, fx=0.8, fy=0.8)
        height, width, channels = img.shape

            # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.6)
        font = cv2.FONT_HERSHEY_PLAIN
        mnist_images = []
        new_boxes_x = []
        text = []
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                new_boxes_x.append(x)
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                digit = img.copy()[y:y+h,x:x+w]
            
                #text.append(image_to_string(digit_rgb))
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                digit_gray = cv2.cvtColor(digit,cv2.COLOR_BGR2GRAY)
                digit_gray = cv2.resize(digit_gray,(28,28),interpolation = cv2.INTER_CUBIC)
                
                #th, digit_thresh = cv2.threshold(digit_gray,50,255,cv2.THRESH_BINARY_INV)
                #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
                #final_thresh = cv2.morphologyEx(digit_thresh, cv2.MORPH_CLOSE, kernel,iterations = 2)
                
                #th, image_thresh = cv2.threshold(digit_gray,150,255,cv2.THRESH_BINARY_INV)
                #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4,4))
                #thresh = cv2.dilate(image_thresh,kernel)
                mnist_images.append((np.float32(digit_gray)/255.0).reshape(28,28,1))
                #cv2.putText(img, label, (x, y + 30), font, 3, color, 2)
        if len(new_boxes_x ) > 0:

            #idxs = np.arange(len(new_boxes_x))
            temp = [ i for i in range(len(new_boxes_x))]
            idxs = [x for y, x in sorted(zip(new_boxes_x,temp))]
            #idxs = sorted(range(len(new_boxes_x)),key = new_boxes_x,reverse = False)
            mnist_data = np.array(mnist_images).reshape(-1,28,28,1)
            mnist_data = mnist_data[idxs]
            temperature = head_model.predict(mnist_data)
            temperature = np.argmax(temperature,axis = 1)
            temperature = list(temperature.reshape(-1,))
            
            final_temperature = [str(t) for t in temperature]
            
            display_temp = "".join(final_temperature[:-1]) + "." + final_temperature[-1]
            #display_temp_ocr = "".join(text[:-1]) + "." + text[-1]
            #print(display_temp)
            #print("The temperature with tesseract is {}".format(display_temp_ocr))
            self.temperatures.append(display_temp)
        
        ending_time = time.time()
        # if ending_time - starting_time > 10:
        #     break
        # cv2.imshow("Image", img)
        # key = cv2.waitKey(1)
        # if key == ord('q'):
        #     break
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

    def destroy(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def get_temperature(self):
        temperature_dict = dict(Counter(self.temperatures))
        self.best_temp = '98.1'
        temperature_sorted = sorted(temperature_dict.items(),key = lambda x : x[1],reverse = True)
        for key,value in temperature_sorted:
            if float(key) >= 95.0 and float(key) <= 105.0:
                self.best_temp = key
                break

        return self.best_temp






# cap.release()
# cv2.destroyAllWindows()

# temperature_dict = dict(Counter(temperatures))
# best_temp = '98.1'
# temperature_sorted = sorted(temperature_dict.items(),key = lambda x : x[1],reverse = True)
# for key,value in temperature_sorted:
#     if float(key) >= 95.0 and float(key) <= 105.0:
#         best_temp = key
#         break

# print("The final temperature is {}".format(best_temp))
