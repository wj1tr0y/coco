import cv2
import json
import random
import os
import shutil
import numpy as np

debug = True
anno_dir = 'Annotations'
patch_dir = 'person_patch'
img_dir = 'ImageSet'

if debug == True:
    if os.path.exists('ImageSet_test'):
        shutil.rmtree('ImageSet_test')
    if os.path.exists('Annotations_test'):
        shutil.rmtree('Annotations_test')
    
    os.mkdir('ImageSet_test')
    os.mkdir('Annotations_test')

    imgs = os.listdir(img_dir)
    imgs = list(np.random.choice(imgs, 10))

    for i in imgs:
        shutil.copy(os.path.join(img_dir, i), 'ImageSet_test')
        shutil.copy(os.path.join(anno_dir, i[:-4]+'.json'), 'Annotations_test')

    anno_dir = 'Annotations_test'
    img_dir = 'ImageSet_test'

patches = os.listdir(patch_dir)
neg_imgs = os.listdir(img_dir)
neg_imgs = [x for x in neg_imgs if 'jpg' in x]
total = len(neg_imgs)
for count, im_name in enumerate(neg_imgs):
    ann = json.load(open(os.path.join(anno_dir, im_name[:-4] + '.json'), 'r'))
    ann['annotation'] = []
    img = cv2.imread(os.path.join(img_dir, im_name))
    success = False
    temp_times = 0
    number = np.random.randint(1,4)
    while not success or number > 0:
        a = random.choice(patches)
        temp_times += 1
        patch = cv2.imread(os.path.join(patch_dir, a))
        ratio = (patch.shape[0] * patch.shape[1])/(float(img.shape[0]) * img.shape[1])
        if ratio < 0.015 and ratio > 0.002:
            x1 = 10
            x2 = img.shape[1] - patch.shape[1] - 10
            y1 = 10
            y2 = img.shape[0] - patch.shape[0] - 10

            x = random.randint(x1,x2 - 1)
            y = random.randint(y1,y2 - 1)
            w = patch.shape[1]
            h = patch.shape[0]
            # get img background
            mask = patch==0
            mask.astype('uint8')
            img[y:y+h, x:x+w] = mask * img[y:y+h, x:x+w]
            img[y:y+h, x:x+w] = img[y:y+h, x:x+w] + patch[:, :]

            ann['annotation'].append({'bbox': [x, y, w, h], 'category_id': 1})
            with open(os.path.join(anno_dir, im_name[:-4] + '.json'), 'w') as new_ann:
                new_ann.writelines(json.dumps(ann, sort_keys=True, indent=2, ensure_ascii=False))

            cv2.imwrite(os.path.join(img_dir, im_name), img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            success = True
            number = number - 1
        if temp_times == 1000:
            success = True
            number = 0
    print('Processed {}/{}'.format(count + 1, total))