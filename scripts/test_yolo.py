import ultralytics
import cv2
from ultralytics import YOLO

if __name__ == '__main__':
    cap = cv2.VideoCapture(2)

    model_path = '../model/yolov8n-pose.pt'

    model = YOLO(model_path)

    while True:

        _,img = cap.read()


        result = model.predict(img)

        img = result[0].plot()

        cv2.imshow('img',img)

        cv2.waitKey(1)

