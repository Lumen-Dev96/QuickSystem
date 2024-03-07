import pandas as pd
from datetime import datetime
import os
import cv2


class DataSegment:

    def __init__(self,athlete):

        self.StreamPixTime = None
        self.EyetrackerTime = None
        self.txt_time_list = None
        self.keyframe_list = None
        self.athlete = athlete
        self.eyetracker_seg_index = None
        self.eyetrackerVideo = None
        self.eyetrackerGaze = None

    def convert_to_datetime(skef,time_str):

        return datetime.strptime(time_str, "%H:%M:%S.%f")

    def find_csv_file(self, root_path):
        for file in os.listdir(root_path):
            if file.endswith('.csv'):
                return os.path.join(root_path, file)
        return None

    def SetTime(self):

        StreamPixPath = os.path.join(self.athlete.folder.ori_realsense,"top")
        csv_file_path = self.find_csv_file(StreamPixPath)
        self.StreamPixTime = csv_file_path

        EyetrackerTimePath = os.path.join(self.athlete.folder.ori, "eyetracker", "time.txt")
        self.EyetrackerTime = EyetrackerTimePath

        self.eyetrackerVideo = os.path.join(self.athlete.folder.ori, "eyetracker", "video.mp4")
        self.eyetrackerGaze = os.path.join(self.athlete.folder.ori, "eyetracker", "gaze.txt")

    def CreateSegFile(self):

        root_path = self.athlete.folder.process

        self.gaze_seg_root_path = os.path.join(root_path,"gaze_seg")
        if not os.path.exists(self.gaze_seg_root_path):
            os.mkdir(self.gaze_seg_root_path)

        self.video_seg_root_path = os.path.join(root_path, "video_seg")
        if not os.path.exists(self.video_seg_root_path):
            os.mkdir(self.video_seg_root_path)


    def RunSeg(self):
        self.SetTime() # 找到stream pix的绝对时间戳和eyetracker 的时间戳
        self.CreateSegFile()
        df = pd.read_csv(self.StreamPixTime)
        txt_file = open(self.EyetrackerTime, 'r', encoding="utf-8")
        next(txt_file)
        self.txt_time_list = [self.convert_to_datetime(line[-13:-1]) for line in txt_file]
        self.keyframe_list = [(self.athlete.key_frame_information[i][0],self.athlete.key_frame_information[i][2]) for i in range(len(self.athlete.key_frame_information))]
        self.eyetracker_seg_index = []

        for sub_keyframe_list in self.keyframe_list:
            start_frame = self.convert_to_datetime(df.iloc[sub_keyframe_list[0], 1][-12:])
            min_diff = min((abs(a - start_frame), i) for i, a in enumerate(self.txt_time_list))
            star_index_in_eyetracker = min_diff[1]  # 输出最近元素在 listA 中的索引
            try:
                end_frame = self.convert_to_datetime(df.iloc[sub_keyframe_list[1] - 2, 1][-12:])
                min_diff2 = min((abs(a - end_frame), i) for i, a in enumerate(self.txt_time_list))
                end_index_in_eyetracker = min_diff2[1]  # 输出最近元素在 listA 中的索引
            except:
                end_frame = self.convert_to_datetime(df.iloc[-1, 1][-12:])
                min_diff2 = min((abs(a - end_frame), i) for i, a in enumerate(self.txt_time_list))
                end_index_in_eyetracker = min_diff2[1]
            self.eyetracker_seg_index.append((star_index_in_eyetracker, end_index_in_eyetracker))
        print("eyetracker Seg index： ", self.eyetracker_seg_index)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = {}
        for i in range(len(self.eyetracker_seg_index)):
            # 将原始变量赋值给新变量名
            name = str("%03d" % i) + ".mp4"
            video_name = os.path.join(self.video_seg_root_path, name)
            video_writer[i] = cv2.VideoWriter(video_name, fourcc, 60, (960, 539))

        cap = cv2.VideoCapture(self.eyetrackerVideo)
        frame_num = 0
        segment_num = 0

        while True:
            _, frame = cap.read()
            if segment_num < len(self.eyetracker_seg_index):
                if frame_num >= int(self.eyetracker_seg_index[segment_num][0]) and frame_num < int(
                        self.eyetracker_seg_index[segment_num][1]):
                    video_writer[segment_num].write(frame)
                    # print("video segment processing")
            else:
                break
            frame_num += 1
            if frame_num > int(self.eyetracker_seg_index[segment_num][1]):
                segment_num += 1

        for i in range(len(self.eyetracker_seg_index)):
            new_txt_name = "txt_writer_{}".format(i)
            name = str("%03d" % i) + ".txt"
            txt_name = os.path.join(self.gaze_seg_root_path, name)
            file_writer = open(file=txt_name, mode="w", encoding="utf-8")
            # globals()[new_txt_name] = open(file=txt_name, mode="w")
            line_num = 0
            with open(file=self.eyetrackerGaze, mode="r", encoding="utf-8") as f_eyetracker_gaze:
                start_gaze = self.eyetracker_seg_index[i][0]
                end_gaze = self.eyetracker_seg_index[i][1]
                eyetracker_gaze_position_lines = f_eyetracker_gaze.readlines()
                for eyetracker_gaze_position_line in eyetracker_gaze_position_lines:
                    if line_num >= int(start_gaze) and line_num < int(end_gaze):

                        file_writer.write(eyetracker_gaze_position_line)
                        # print("gaze segment processing")
                    if line_num > int(end_gaze):
                        break

                    line_num += 1

        txt_file.close()


    def RunSegPendo(self):
        self.SetTime() # 找到stream pix的绝对时间戳和eyetracker 的时间戳
        self.CreateSegFile()
        df = pd.read_csv(self.StreamPixTime)
        txt_file = open(self.EyetrackerTime, 'r', encoding="utf-8")
        next(txt_file)
        self.txt_time_list = [self.convert_to_datetime(line[-13:-1]) for line in txt_file]
        self.keyframe_list = [(self.athlete.key_frame_information[i][0],self.athlete.key_frame_information[i][2]) for i in range(len(self.athlete.key_frame_information))]
        self.eyetracker_seg_index = []

        for sub_keyframe_list in self.keyframe_list:
            start_frame = self.convert_to_datetime(df.iloc[sub_keyframe_list[0], 1][-12:])
            min_diff = min((abs(a - start_frame), i) for i, a in enumerate(self.txt_time_list))
            star_index_in_eyetracker = min_diff[1]  # 输出最近元素在 listA 中的索引
            try:
                end_frame = self.convert_to_datetime(df.iloc[sub_keyframe_list[1] - 2, 1][-12:])
                min_diff2 = min((abs(a - end_frame), i) for i, a in enumerate(self.txt_time_list))
                end_index_in_eyetracker = min_diff2[1]  # 输出最近元素在 listA 中的索引
            except:
                end_frame = self.convert_to_datetime(df.iloc[-1, 1][-12:])
                min_diff2 = min((abs(a - end_frame), i) for i, a in enumerate(self.txt_time_list))
                end_index_in_eyetracker = min_diff2[1]
            self.eyetracker_seg_index.append((star_index_in_eyetracker, end_index_in_eyetracker))
        print("eyetracker Seg index： ", self.eyetracker_seg_index)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = {}
        for i in range(len(self.eyetracker_seg_index)):
            # 将原始变量赋值给新变量名
            name = str("%03d" % i) + ".mp4"
            video_name = os.path.join(self.video_seg_root_path, name)
            video_writer[i] = cv2.VideoWriter(video_name, fourcc, 60, (960, 539))

        cap = cv2.VideoCapture(self.eyetrackerVideo)
        frame_num = 0
        segment_num = 0

        while True:
            _, frame = cap.read()
            if segment_num < len(self.eyetracker_seg_index):
                if frame_num >= int(self.eyetracker_seg_index[segment_num][0]) and frame_num < int(
                        self.eyetracker_seg_index[segment_num][1]):
                    video_writer[segment_num].write(frame)
                    # print("video segment processing")
            else:
                break
            frame_num += 1
            if frame_num > int(self.eyetracker_seg_index[segment_num][1]):
                segment_num += 1

        for i in range(len(self.eyetracker_seg_index)):
            new_txt_name = "txt_writer_{}".format(i)
            name = str("%03d" % i) + ".txt"
            txt_name = os.path.join(self.gaze_seg_root_path, name)
            file_writer = open(file=txt_name, mode="w", encoding="utf-8")
            # globals()[new_txt_name] = open(file=txt_name, mode="w")
            line_num = 0
            with open(file=self.eyetrackerGaze, mode="r", encoding="utf-8") as f_eyetracker_gaze:
                start_gaze = self.eyetracker_seg_index[i][0]
                end_gaze = self.eyetracker_seg_index[i][1]
                eyetracker_gaze_position_lines = f_eyetracker_gaze.readlines()
                for eyetracker_gaze_position_line in eyetracker_gaze_position_lines:
                    if line_num >= int(start_gaze) and line_num < int(end_gaze):

                        file_writer.write(eyetracker_gaze_position_line)
                        # print("gaze segment processing")
                    if line_num > int(end_gaze):
                        break

                    line_num += 1

        txt_file.close()


# if __name__ == "__main__":