import xml.etree.ElementTree as ElementTree


if __name__ == '__main__':
    xml_file = "../data/2024-03-28/Leung Yuk Wing_002/synchronize/data.xml"

    line_data = []
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    line_index = 0
    temp = []

    for keypoint_elem in root.findall('keypoint'):
        timestamp = keypoint_elem.find('timestamp').text.strip()

        handwriting_elem = keypoint_elem.find('handwriting')
        x = handwriting_elem.find('x').text.strip()
        y = handwriting_elem.find('y').text.strip()
        pressure = handwriting_elem.find('pressure').text

        if x == 'None' or y == 'None':
            if temp:
                line_data.append(temp)
                temp = []
        else:
            temp.append([timestamp, x, y, pressure])

    if temp:
        line_data.append(temp)

    print(line_data)



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
