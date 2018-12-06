# import cv2
# import argparse
# import os
# import shutil
# import subprocess 
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description = "run test and get all result")
#     parser.add_argument("video", 
#         help = "path of test video")
#     parser.add_argument("--gpuid",
#         help = "The gpu chosen to run the model.", required=True)

#     args = parser.parse_args()
#     assert len(args.gpuid) == 1, "You only need to choose one gpu. But {} gpus are chosen.".format(args.gpuid)

#     video_name = args.video

#     if not os.path.exists(video_name):
#         print("{} doesn't exist.".format(video_name))

#     frame_save_dir = 'videocap'
#     if os.path.exists(frame_save_dir):
#         shutil.rmtree(frame_save_dir)
#         os.mkdir(frame_save_dir)
#     else:
#         os.mkdir(frame_save_dir)

#     cap = cv2.VideoCapture(video_name)
#     frame_count = 1
#     success = True
#     while(success):
#         success, frame = cap.read()
#         if success:
#             print('Reading frames: {}\r'.format(frame_count), end='')
#             cv2.imwrite(os.path.join(frame_save_dir, 'frame{}.jpg'.format(frame_count)), frame)
#             frame_count += 1
#         else:
#             print('')
#     cap.release()

#     print('Detecting pedestrian.....')
#     cmd = "python run_test.py --gpuid 0 --out-dir result --test-set videocap"
#     print(cmd)
#     process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
#     output = process.communicate()
#     print(output)

import cv2
import os

cap = cv2.VideoCapture('test.avi')
fps = int(cap.get(cv2.CAP_PROP_FPS))
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
codec = int(cap.get(cv2.CAP_PROP_FOURCC))
videoWriter = cv2.VideoWriter('oto_other.avi', cv2.VideoWriter_fourcc('X','V','I','D'), fps, size)
frame_name = os.listdir('result')
frame_name = sorted(frame_name, key=lambda x: int(x[5:-9]))
for i in frame_name:
    frame = cv2.imread('result/' + i)
    videoWriter.write(frame)
videoWriter.release()
