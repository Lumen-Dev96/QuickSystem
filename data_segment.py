import os
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

    def set_file_path(self):
        # csv_file_path = self.find_csv_file(realsense_time_path)
        self.realsense_time_path = os.path.join(self.filepath, "realsense", "realsense_time.txt")

        self.eyetracker_time_path = os.path.join(self.filepath, "eyetracker", "time.txt")
        self.eyetracker_video_path = os.path.join(self.filepath, "eyetracker", "video.mp4")
        self.eyetracker_gaze_path = os.path.join(self.filepath, "eyetracker", "gaze.txt")

        self.handwriting_time_path = os.path.join(self.filepath, "handwriting", "handwriting_time.txt")

    def create_seg_file(self):
        self.output_path = os.path.join(self.synchronize_filepath)
        create_file_if_not_exists(self.output_path)

    def run_seg(self):
        print('Start data processing...')
        self.set_file_path()
        self.create_seg_file()
        data = []
        # df = pd.read_csv(self.realsense_time)
        realsense_time = open(self.realsense_time_path, 'r', encoding='utf-8')
        eyetracker_time = open(self.eyetracker_time_path, 'r', encoding="utf-8")
        handwriting_time = open(self.handwriting_time_path, 'r', encoding="utf-8")

        next(eyetracker_time)
        self.eyetracker_txt_time_list = [convert_to_datetime(line[-13:-1]) for line in eyetracker_time]
        self.realsense_txt_time_list = [convert_to_datetime(line[-13:-1]) for line in realsense_time]
        self.handwriting_txt_time_list = [convert_to_datetime(line[11:22]) for line in handwriting_time]
        realsense_time.close()
        eyetracker_time.close()
        handwriting_time.close()

        realsense_time_index_list = []
        for timestamp in self.eyetracker_txt_time_list:
            # min_diff return 0 -> microseconds, 1 -> index
            min_diff = min((abs(time - timestamp), index) for index, time in enumerate(self.realsense_txt_time_list))
            realsense_time_index_list.append(min_diff[1])

        eyetracker_time_index_list = []
        for timestamp in self.handwriting_txt_time_list:
            # min_diff return 0 -> microseconds, 1 -> index
            min_diff = min((abs(time - timestamp), index) for index, time in enumerate(self.eyetracker_txt_time_list))
            eyetracker_time_index_list.append(min_diff[1])

        # Read eyetracker gaze data
        eyetracker_gaze = []
        with open(self.eyetracker_gaze_path, 'r') as file:
            for line in file:
                line = line.strip()
                items = line.split()
                eyetracker_gaze.append(items)

        # Read handwriting data
        handwriting_data = []
        with open(self.handwriting_time_path, 'r') as file:
            for line in file:
                line = line.strip()
                row = [item.strip() for item in line.split(',')]
                handwriting_data.append(row)

        # Read eyetracker time data
        eyetracker_time = []
        with open(self.eyetracker_time_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                eyetracker_time.append(line)

        line = ""
        for index, timestamp in enumerate(eyetracker_time):
            gaze1 = eyetracker_gaze[index][0]
            gaze2 = eyetracker_gaze[index][1]

            if index in eyetracker_time_index_list:
                x = handwriting_data[index][1]
                y = handwriting_data[index][2]
                pressure = handwriting_data[index][3]
            else:
                x = None
                y = None
                pressure = None

            line += "{}, {}, {}, {}, {}, {}\n".format(timestamp, gaze1, gaze2, x, y, pressure)

        output_data_path = os.path.join(self.synchronize_filepath, 'data.txt')
        with open(output_data_path, 'w') as file:
            file.write(line)

        print('Data processed successfully!')
