from imutils import paths
from collections import OrderedDict
import numpy as np
import argparse
import imutils
import json
import dlib
import cv2
import sys
import os
from facealigner import FaceAligner



def shape_to_np(shape, dtype="int"):
	# initialize the list of (x, y)-coordinates
	coords = np.zeros((68, 2), dtype=dtype)
	# loop over the 68 facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, 68):
		coords[i] = (shape.part(i).x, shape.part(i).y)
	# return the list of (x, y)-coordinates
	return coords

FACIAL_LANDMARKS_IDXS = OrderedDict([
	("mouth", (48, 68)),
	("inner_mouth", (60, 68)),
	("right_eyebrow", (17, 22)),
	("left_eyebrow", (22, 27)),
	("right_eye", (36, 42)),
	("left_eye", (42, 48)),
	("nose", (27, 36)),
	("jaw", (0, 17))
])

def overlay_image(bg, fg, fgMask, coords):
	# grab the foreground spatial dimensions (width and height),
	# then unpack the coordinates tuple (i.e., where in the image
	# the foreground will be placed)
	(sH, sW) = fg.shape[:2]
	(x, y) = coords
	# the overlay should be the same width and height as the input
	# image and be totally blank *except* for the foreground which
	# we add to the overlay via array slicing
	overlay = np.zeros(bg.shape, dtype="uint8")
	overlay[y:y + sH, x:x + sW] = fg
	# the alpha channel, which controls *where* and *how much*
	# transparency a given region has, should also be the same
	# width and height as our input image, but will contain only
	# our foreground mask
	alpha = np.zeros(bg.shape[:2], dtype="uint8")
	alpha[y:y + sH, x:x + sW] = fgMask
	alpha = np.dstack([alpha] * 3)
	# perform alpha blending to merge the foreground, background,
	# and alpha channel together
	output = alpha_blend(overlay, bg, alpha)
	# return the output image
	return output

def alpha_blend(fg, bg, alpha):
	# convert the foreground, background, and alpha layers from
	# unsigned 8-bit integers to floats, making sure to scale the
	# alpha layer to the range [0, 1]
	fg = fg.astype("float")
	bg = bg.astype("float")
	alpha = alpha.astype("float") / 255
	# perform alpha blending
	fg = cv2.multiply(alpha, fg)
	bg = cv2.multiply(1 - alpha, bg)
	# add the foreground and background to obtain the final output
	# image
	output = cv2.add(fg, bg)
	
	# return the output image
	return output.astype("uint8")


# load the JSON configuration file and the "Deal With It" sunglasses
# and associated mask
#config = json.loads(open(args["config"]).read())
#sunglass_path = os.path.join(os.path.join("..",'data_aug'),'sunglass.png')
#raw_sg = cv2.imread(sunglass_path,cv2.IMREAD_UNCHANGED)
#sg = raw_sg[:,:,:3]
#sgMask = raw_sg[:,:,3]
# delete any existing temporary directory (if it exists) and then
# create a new, empty directory where we'll store each individual
# frame in the GIF
#shutil.rmtree(config["temp_dir"], ignore_errors=True)
#os.makedirs(config["temp_dir"])

print("[INFO] loading models...")
face_detector_prototxt_path = os.path.join("..",os.path.join("face_detector","deploy.prototxt"))
face_detector_config_path = os.path.join("..",os.path.join("face_detector","res10_300x300_ssd_iter_140000.caffemodel"))
detector = cv2.dnn.readNetFromCaffe(face_detector_prototxt_path,
	face_detector_config_path)
predictor = dlib.shape_predictor(os.path.join("..",os.path.join("data","shape_predictor_68_face_landmarks.dat")))


# load the input image and construct an input blob from the image


imagepaths = []
dirpath = os.path.join("..","Dataset")
for label in os.listdir(dirpath):
	for i,imagep in enumerate(os.listdir(os.path.join(dirpath,label))):
		if imagep.startswith("{}01".format(label)):
			imagepath = os.path.join(os.path.join(dirpath,label),imagep)
			imagepaths.append(imagepath)
		else:
			continue
	

save_dir = os.path.join('..','Dataset_aug_advanced')
if not os.path.exists(save_dir):
	os.mkdir(save_dir)

for i,imagepath in enumerate(imagepaths):


	sunglass_path = os.path.join(os.path.join("..",'data_aug'),'sunglass.png')
	raw_sg = cv2.imread(sunglass_path,cv2.IMREAD_UNCHANGED)
	sg = raw_sg[:,:,:3]
	sgMask = raw_sg[:,:,3]   
	image = cv2.imread(imagepath)
	(H, W) = image.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
		(300, 300), (104.0, 177.0, 123.0))
	# pass the blob through the network and obtain the detections
	print("[INFO] computing object detections...")
	detector.setInput(blob)
	detections = detector.forward()
	# we'll assume there is only one face we'll be applying the "Deal
	# With It" sunglasses to so let's find the detection with the largest
	# probability
	i = np.argmax(detections[0, 0, :, 2])
	confidence = detections[0, 0, i, 2]
	# filter out weak detections
	if confidence < 0.5:
		print("[INFO] no reliable faces found")
		sys.exit(0)

	# compute the (x, y)-coordinates of the bounding box for the face
	box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
	(startX, startY, endX, endY) = box.astype("int")
	print((endX - startX))
	print(endY - startY)
	# construct a dlib rectangle object from our bounding box coordinates
	# and then determine the facial landmarks for the face region
	rect = dlib.rectangle(int(startX), int(startY), int(endX), int(endY))
	shape = predictor(image,rect)
	shape = shape_to_np(shape)
	# grab the indexes of the facial landmarks for the left and right
	# eye, respectively, then extract (x, y)-coordinates for each eye
	(lStart, lEnd) = FACIAL_LANDMARKS_IDXS["left_eye"]
	(rStart, rEnd) = FACIAL_LANDMARKS_IDXS["right_eye"]
	leftEyePts = shape[lStart:lEnd]
	rightEyePts = shape[rStart:rEnd]

	leftEyeCenter = leftEyePts.mean(axis=0).astype("int")
	rightEyeCenter = rightEyePts.mean(axis=0).astype("int")
	# compute the angle between the eye centroids
	dY = rightEyeCenter[1] - leftEyeCenter[1]
	dX = rightEyeCenter[0] - leftEyeCenter[0]
	angle = np.degrees(np.arctan2(dY, dX)) - 180

	# rotate the sunglasses image by our computed angle, ensuring the
	# sunglasses will align with how the head is tilted
	sg = imutils.rotate_bound(sg, angle)
	# the sunglasses shouldn't be the *entire* width of the face and
	# ideally should just cover the eyes -- here we'll do a quick
	# approximation and use 90% of the face width for the sunglasses
	# width
	sgW = int((endX - startX) * 0.9)
	sg = imutils.resize(sg, width=sgW)
	# our sunglasses contain transparency (the bottom parts, underneath
	# the lenses and nose) so in order to achieve that transparency in
	# the output image we need a mask which we'll use in conjunction with
	# alpha blending to obtain the desired result -- here we're binarizing
	# our mask and performing the same image processing operations as
	# above

	#sgMask = cv2.cvtColor(sgMask, cv2.COLOR_BGR2GRAY)
	sgMask = cv2.threshold(sgMask, 0, 255, cv2.THRESH_BINARY)[1]
	sgMask = imutils.rotate_bound(sgMask, angle)
	sgMask = imutils.resize(sgMask, width=sgW, inter=cv2.INTER_NEAREST)



	shiftX = int(sg.shape[1] * 0.25)
	shiftY = int(sg.shape[0] * 0.35)


	output = overlay_image(image, sg, sgMask,
			(rightEyeCenter[0] - shiftX, rightEyeCenter[1] - shiftY))





	label = imagepath.split(os.path.sep)[-2]
	label_path = os.path.join(save_dir,label)
	if not os.path.exists(label_path):
		os.mkdir(label_path)
	cv2.imwrite(os.path.join(label_path,"{}glass{}.jpg".format(label,str(i+1))),output)