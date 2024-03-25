import os
from util.common import create_file_if_not_exists, convert_to_datetime
import xml.etree.ElementTree as ElementTree


class DataSegment:

    def __init__(self, filepath):

        self.synchronize_filepath = os.path.join(filepath, 'synchronize')
        self.filepath = filepath

        # raw data set path
        self.realsense_time_path = None
        self.realsense_joint_path = None

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

        self.root = ElementTree.Element("root")


    def set_file_path(self):
        # csv_file_path = self.find_csv_file(realsense_time_path)
        self.realsense_time_path = os.path.join(self.filepath, "realsense", "realsense_time.txt")
        self.realsense_joint_path = os.path.join(self.filepath, "realsense", "joint.xml")

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
        # df = pd.read_csv(self.realsense_time)
        realsense_time = open(self.realsense_time_path, 'r', encoding='utf-8')
        eyetracker_time = open(self.eyetracker_time_path, 'r', encoding="utf-8")
        handwriting_time = open(self.handwriting_time_path, 'r', encoding="utf-8")

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

        # Read realsense skeleton data
        joint_data = []
        tree = ElementTree.parse(self.realsense_joint_path)
        root = tree.getroot()
        for keypoint_elem in root.findall('keypoint'):
            timestamp = keypoint_elem.find('timestamp').text.strip()

            left_elbow_angle_elem = keypoint_elem.find('left_elbow_angle')
            if left_elbow_angle_elem is not None:
                left_elbow_angle = float(left_elbow_angle_elem.text)
            else:
                left_elbow_angle = None

            right_elbow_angle_elem = keypoint_elem.find('right_elbow_angle')
            if right_elbow_angle_elem is not None:
                right_elbow_angle = float(right_elbow_angle_elem.text)
            else:
                right_elbow_angle = None

            positions = []
            for position_elem in keypoint_elem.findall('position'):
                x = float(position_elem.find('x').text)
                y = float(position_elem.find('y').text)
                confidence = float(position_elem.find('confidence').text)
                position = Position(x, y, confidence)
                positions.append(position)

            keypoint = Keypoint(timestamp, left_elbow_angle, right_elbow_angle, positions)
            joint_data.append(keypoint)

        # Start Synchronizing
        # line = ""
        tree = ElementTree.ElementTree(self.root)
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

            joint_keypoint = joint_data[realsense_time_index_list[index]]
            left_elbow_angle = joint_keypoint.left_elbow_angle
            right_elbow_angle = joint_keypoint.right_elbow_angle

            # Construct xml
            keypoint_element = ElementTree.SubElement(self.root, "keypoint")
            time_element = ElementTree.SubElement(keypoint_element, "timestamp")
            time_element.text = timestamp

            left_elbow_element = ElementTree.SubElement(keypoint_element, "left_elbow_angle")
            left_elbow_element.text = str(left_elbow_angle)
            right_elbow_element = ElementTree.SubElement(keypoint_element, "right_elbow_angle")
            right_elbow_element.text = str(right_elbow_angle)

            for position in joint_keypoint.positions:
                # save 17 different joints positions: (x, y, confidence)
                position_element = ElementTree.SubElement(keypoint_element, "position")
                x_element = ElementTree.SubElement(position_element, "x")
                x_element.text = str(position.x)
                y_element = ElementTree.SubElement(position_element, "y")
                y_element.text = str(position.y)
                confidence_element = ElementTree.SubElement(position_element, "confidence")
                confidence_element.text = str(position.confidence)

            eyetracker_element = ElementTree.SubElement(keypoint_element, "eyetracker")
            gaze_x_element = ElementTree.SubElement(eyetracker_element, "gaze_x")
            gaze_x_element.text = str(gaze1)
            gaze_y_element = ElementTree.SubElement(eyetracker_element, "gaze_y")
            gaze_y_element.text = str(gaze2)

            handwriting_element = ElementTree.SubElement(keypoint_element, "handwriting")
            handwriting_x_element = ElementTree.SubElement(handwriting_element, "x")
            handwriting_x_element.text = str(x)
            handwriting_y_element = ElementTree.SubElement(handwriting_element, "y")
            handwriting_y_element.text = str(y)
            handwriting_pressure_element = ElementTree.SubElement(handwriting_element, "pressure")
            handwriting_pressure_element.text = str(pressure)

            # line += "{}, {}, {}, {}, {}, {}\n".format(timestamp, gaze1, gaze2, x, y, pressure)

        output_data_path = os.path.join(self.synchronize_filepath, 'data.xml')
        tree.write(output_data_path, encoding="utf-8", xml_declaration=True)
        # with open(output_data_path, 'w') as file:
        #     file.write(line)

        print('Data processed successfully!')


class Keypoint:
    def __init__(self, timestamp, left_elbow_angle, right_elbow_angle, positions):
        self.timestamp = timestamp
        self.left_elbow_angle = left_elbow_angle
        self.right_elbow_angle = right_elbow_angle
        self.positions = positions


class Position:
    def __init__(self, x, y, confidence):
        self.x = x
        self.y = y
        self.confidence = confidence