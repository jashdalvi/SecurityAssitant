from tensorflow.keras.preprocessing.image import img_to_array,load_img,ImageDataGenerator
import numpy as np
from imutils import paths
import os

aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                        height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                        horizontal_flip=True, fill_mode="nearest")

dataset_path = os.path.join('..','Dataset')
dataset_aug_advanced_path = os.path.join("..","Dataset_aug_advanced")
dataset_aug_path = os.path.join("..",'Dataset_aug')
if not os.path.exists(dataset_aug_path):
    os.mkdir(dataset_aug_path)
else:
    imagepaths_aug = paths.list_images(dataset_aug_path)
    for imagepath in imagepaths_aug:
        os.remove(imagepath)



imagepaths = paths.list_images(dataset_path)
imagepaths_aug_advanced = paths.list_images(dataset_aug_advanced_path)
super_total = 0
for i,imagep in enumerate(imagepaths):
    label = imagep.split(os.path.sep)[-2]
    image = load_img(imagep)
    image = img_to_array(image)
    image = np.expand_dims(image,axis = 0)
    save_to_dir = os.path.join(dataset_aug_path,label)
    if not os.path.exists(save_to_dir):
        os.mkdir(save_to_dir)
    imageGen = aug.flow(image, batch_size=1, save_to_dir=save_to_dir,save_prefix=label, save_format="jpg")
    total = 0
    for imageg in imageGen:
        super_total += 1
        total += 1
        if total == 50:
            break
    if super_total % 100 == 0 :
        print('Processed {} images'.format(super_total))

for i,imagep in enumerate(imagepaths_aug_advanced):
    label = imagep.split(os.path.sep)[-2]
    image = load_img(imagep)
    image = img_to_array(image)
    image = np.expand_dims(image,axis = 0)
    save_to_dir = os.path.join(dataset_aug_path,label)
    if not os.path.exists(save_to_dir):
        os.mkdir(save_to_dir)
    imageGen = aug.flow(image, batch_size=1, save_to_dir=save_to_dir,save_prefix=label, save_format="jpg")
    total = 0
    for imageg in imageGen:
        super_total += 1
        total += 1
        if total % 100 == 0:
            break
    if super_total % 100 == 0 :
        print('Processed {} images'.format(super_total))




print("Augmented {} images in total".format(super_total))