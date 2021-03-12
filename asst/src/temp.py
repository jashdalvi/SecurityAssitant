import cv2
import os
import imutils

beard_path = os.path.join(os.path.join("..",'data_aug'),'beard1.png')

image = cv2.imread(beard_path,cv2.IMREAD_UNCHANGED)

imagebgr = image[:,:,-1]
print(imagebgr.shape)
imagebgr = imagebgr[11:331,39:440]
#imagebgr = imutils.rotate_bound(imagebgr,30)
imagebgr = cv2.resize(imagebgr,(224,224))
imagebgr = imutils.rotate_bound(imagebgr,30)
cv2.imshow("Beard",(cv2.bitwise_not(imagebgr)))
cv2.waitKey(0)
cv2.destroyAllWindows()