from ultralytics import YOLO
import cv2
import time
import pandas
import numpy as np
import pandas as pd



if __name__ == '__main__':

    # model = YOLO(r"D:\RA\Boccia\hksi_9_29\best.pt")
    model = YOLO('yolov8x-pose.pt')
    #
    video_path = r"D:\RA\big system - key frame\KeyFrameCut\cut_video\wing2\right_far\2.avi"
    # img_path = r"G:\Boccia\BOCCIA_quick_data\images\train\images\1 (2597).jpg"

    # img = cv2.imread(img_path)
    key_athlete_right_far = r"D:\RA\big system - key frame\KeyFrameCut\cut_video\wing2\right_far_info\2\athlete.xlsx"
    cap = cv2.VideoCapture(video_path)

    # # results = model.track(source=video_path, conf=0.6, iou=0.5, show=True,tracker='botsort.yaml')
    # results = model.track(source=video_path, tracker='botsort.yaml',show=True)
    # # results = model.track(source=video_path, conf=0.5, iou=0.5, show=True)

    frame = 0
    # 读取key athlete 的坐标
    df = pd.read_excel(key_athlete_right_far)
    df_frame = 0  # 用来记录需要遍历key athlete的第几行

    # while cap.isOpened():
    #
    #     _, img = cap.read()
    #     mask_box = eval(df.iloc[df_frame, 0])
    #
    #     #
    #     if _:
    #
    #             start = time.time()
    #
    #             mask = np.zeros_like(img)
    #             mask[mask_box[1]:mask_box[3], mask_box[0]:mask_box[2]] = img[mask_box[1]:mask_box[3],
    #                                                                      mask_box[0]:mask_box[2]]
    #
    #             result =model.predict(mask,conf = 0.5)
    #
    #
    #
    #             image = result[0].plot()
    #
    #             # names = result[0].names
    #             #
    #             # for d in result[0].boxes:
    #             #     _class = int(d.cls)
    #             #     print(names[_class])
    #
    #             image = cv2.resize(image, (int(image.shape[1] * 0.5), int(image.shape[0] * 0.5)))
    #
    #             cv2.imshow("img", image)
    #
    #             cv2.waitKey(1)
    #             end = time.time()
    #             print("&&&&&&&&&&&&&&&time: ", end - start)
    #
    #
    #     else:
    #         break
    #     frame = frame + 1


    #####  图片 ###################
    img_path =r"E:\dataset\joint_new\a1.jpg"
    img = cv2.imread(img_path)
    result = model.predict(img, conf=0.5)
    image = result[0].plot()
    image = cv2.resize(image, (int(image.shape[1] * 0.5), int(image.shape[0] * 0.5)))

    cv2.imshow("img", image)

    cv2.waitKey(0)

