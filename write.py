import os
os.system('python ./yolov5/detect.py --weights ./yolov5/runs/train/exp/weights/best.pt --img 416 --conf 0.25 --source ./yolov5/runs/train/exp/test_images')
