import data_segment


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


if __name__ == '__main__':
    xml_file = "../data/2024-03-22/Leung Yuk Wing_002/realsense/joint.xml"

    file_path = '../data/2024-03-25/Leung Yuk Wing_002'
    print('test start')
    segment = data_segment.DataSegment(file_path)
    segment.run_seg()

    # 打印对象数组数据
    # print(keypoints)
    # for keypoint in keypoints:
    #     print('Timestamp:', keypoint.timestamp)
    #     print('Left Elbow Angle:', keypoint.left_elbow_angle)
    #     print('Right Elbow Angle:', keypoint.right_elbow_angle)
    #     print('Positions:')
    #     for position in keypoint.positions:
    #         print('  X:', position.x)
    #         print('  Y:', position.y)
    #         print('  Confidence:', position.confidence)
    #     print('---')
