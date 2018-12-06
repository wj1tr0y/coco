import cv2
import json
import os
import random
import time
ann_names = os.listdir('Annotations')
if not os.path.exists('person_patch'):
    os.mkdir('person_patch')
areas = []
for count, ann_name in enumerate(ann_names):
    im_name = ann_name[:ann_name.index('.')] + '.jpg'
    img = cv2.imread(os.path.join('ImageSet', im_name))
    with open(os.path.join('Annotations', ann_name), 'r') as f:
        ann = json.load(f)
        height = ann['image']['height']
        width = ann['image']['width']
    for i in ann['annotation']:
        x1 = i['bbox'][0]
        y1 = i['bbox'][1]
        w = i['bbox'][2]
        h = i['bbox'][3]
        area = float(w) * h
        if(area/(height*width) < 0.0023 and area/(height*width) > 0.00095):
            patch = img[int(y1):int(y1+h), int(x1):int(x1+w)]
            cv2.imwrite(os.path.join('person_patch', str(count) + str(int(time.time())) + '.jpg'), patch)