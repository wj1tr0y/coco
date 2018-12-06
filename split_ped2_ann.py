import argparse
from collections import OrderedDict
import json
import os
from pprint import pprint
import sys
import cv2
sys.path.append(os.path.dirname(sys.path[0]))


HOMEDIR = os.path.expanduser("~")
DATASETDIR = os.path.join(HOMEDIR, 'data/newped/')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "convert ped annotation to MSCOCO-style json annotation file. And split Annotation file into single files by image")
    parser.add_argument("--out-dir",
            help = "The output directory where we store the annotation per image.")
    args = parser.parse_args()

    out_dir = os.path.join(DATASETDIR, args.out_dir)
    if out_dir:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
    for subset in range(1, 10):
        annofile_dir = os.path.join(DATASETDIR, str(subset))
        imageset_dir = os.path.join(DATASETDIR, str(subset))

        ann_filenames = os.path.join(annofile_dir, 'multi_person.json')
        annotations = json.load(open(ann_filenames, 'r'))
        for ann in annotations:
            im_name = ann['filename']
            if len(ann['annotations']) == 0:
                continue
            with open(os.path.join(out_dir, im_name[:-4] + '.json'), 'w') as new_ann:
                try:
                    img = cv2.imread(os.path.join(imageset_dir, im_name))
                    height, width, _ = img.shape
                except:
                    print(im_name)
                    continue
                json_format = {"annotation": [], 
                                "image": {
                                    "file_name": im_name,
                                    "height": height,
                                    "width": width}}
                del img
                for bbox in ann['annotations']:
                    x = bbox['x']
                    y = bbox['y']
                    w = bbox['width']
                    h = bbox['height']
                    if x < 0:
                        x = 0
                    if y < 0:
                        y = 0
                    if x > width:
                        x = width
                    if y > height:
                        y = height
                    if x + w > width:
                        w = width - x
                    if y + h > height:
                        h = height - y
                    temp = {"category_id": 1, "iscrowd": 0, "bbox": [x, y, w, h],}
                    json_format["annotation"].append(temp)
                new_ann.writelines(json.dumps(json_format, sort_keys=True, indent=2, ensure_ascii=False))

        print(subset)
