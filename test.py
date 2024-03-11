import data_segment

if __name__ == '__main__':
    file_path = './data/2024-03-08/Yeung Hiu Lam_001'
    print('test start')
    segment = data_segment.DataSegment(file_path)
    segment.run_seg()
