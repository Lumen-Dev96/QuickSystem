import xml.etree.ElementTree as ET


def xml_to_list(element):
    result = {}
    result['tag'] = element.tag
    result['text'] = element.text

    if len(element) > 0:
        result['children'] = [xml_to_list(child) for child in element]
    else:
        result['children'] = []

    return result


def read_xml_data(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    data_list = [xml_to_list(child) for child in root]

    return data_list


if __name__ == '__main__':
    xml_file = "../data/2024-03-12/Leung Yuk Wing_003/realsense/joint.xml"


    data_list = read_xml_data(xml_file)
    print(data_list)
