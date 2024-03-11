import os
import cv2
from util.common import create_file_if_not_exists, convert_to_datetime


class DataSegment:

    def __init__(self, filepath):

        self.synchronize_filepath = os.path.join(filepath, 'synchronize')
        self.filepath = filepath

        # raw data set path
        self.realsense_time_path = None

        self.eyetracker_time_path = None
        self.eyetracker_video_path = None
        self.eyetracker_gaze_path = None
        self.eyetracker_seg_index = None

        self.handwriting_time_path = None

        # data set path after process
        self.output_path = None
        self.video_seg_root_path = None

        self.eyetracker_txt_time_list = None
        self.realsense_txt_time_list = None
        self.handwriting_txt_time_list = None
        self.keyframe_list = None

    def set_time_file_path(self):
        # csv_file_path = self.find_csv_file(realsense_time_path)
        self.realsense_time_path = os.path.join(self.filepath, "realsense", "realsense_time.txt")

        self.eyetracker_time_path = os.path.join(self.filepath, "eyetracker", "time.txt")
        self.eyetracker_video_path = os.path.join(self.filepath, "eyetracker", "video.mp4")
        self.eyetracker_gaze_path = os.path.join(self.filepath, "eyetracker", "gaze.txt")

        self.handwriting_time_path = os.path.join(self.filepath, "handwriting", "handwriting_time.txt")

    def create_seg_file(self):
        self.output_path = os.path.join(self.synchronize_filepath, "data.txt")
        create_file_if_not_exists(self.output_path)

    def run_seg(self):
        self.set_time_file_path()
        self.create_seg_file()
        # df = pd.read_csv(self.realsense_time)
        realsense_time = open(self.realsense_time_path, 'r', encoding='utf-8')
        eyetracker_time = open(self.eyetracker_time_path, 'r', encoding="utf-8")
        handwriting_time = open(self.handwriting_time_path, 'r', encoding="utf-8")

        next(eyetracker_time)
        self.eyetracker_txt_time_list = [convert_to_datetime(line[-13:-1]) for line in eyetracker_time]
        self.realsense_txt_time_list = [convert_to_datetime(line[-13:-1]) for line in realsense_time]
        self.handwriting_txt_time_list = [convert_to_datetime(line[11:22]) for line in handwriting_time]

        for timestamp in self.eyetracker_txt_time_list:
            min_diff1 = min((abs(time - timestamp), index) for index, time in enumerate(self.realsense_txt_time_list))
            min_diff2 = min((abs(time - timestamp), index) for index, time in enumerate(self.handwriting_txt_time_list))
            realsense_time_index = min_diff1[1]
            handwriting_time_index = min_diff1[2]

        return

        self.eyetracker_seg_index = []

        for sub_keyframe_list in self.keyframe_list:
            start_frame = convert_to_datetime(df.iloc[sub_keyframe_list[0], 1][-12:])
            min_diff = min((abs(a - start_frame), i) for i, a in enumerate(self.eyetracker_txt_time_list))
            star_index_in_eyetracker = min_diff[1]  # 输出最近元素在 listA 中的索引
            try:
                end_frame = convert_to_datetime(df.iloc[sub_keyframe_list[1] - 2, 1][-12:])
                min_diff2 = min((abs(a - end_frame), i) for i, a in enumerate(self.eyetracker_txt_time_list))
                end_index_in_eyetracker = min_diff2[1]  # 输出最近元素在 listA 中的索引
            except:
                end_frame = convert_to_datetime(df.iloc[-1, 1][-12:])
                min_diff2 = min((abs(a - end_frame), i) for i, a in enumerate(self.eyetracker_txt_time_list))
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

        cap = cv2.VideoCapture(self.eyetracker_video_path)
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
            txt_name = os.path.join(self.output_path, name)
            file_writer = open(file=txt_name, mode="w", encoding="utf-8")
            # globals()[new_txt_name] = open(file=txt_name, mode="w")
            line_num = 0
            with open(file=self.eyetracker_gaze_path, mode="r", encoding="utf-8") as f_eyetracker_gaze:
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

        eyetracker_time.close()
