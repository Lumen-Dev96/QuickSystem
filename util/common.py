import os
import time


def get_time():
    now = time.localtime()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
    return now_time


def create_file_if_not_exists(file_path):
    if not os.path.exists(file_path):
        print(file_path, " is not exists")
        os.makedirs(file_path)
    else:
        print(file_path, " is exists")
        pass
