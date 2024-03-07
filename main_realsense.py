import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Boccia_UI import *
import cv2
import zmq
from msgpack import unpackb, packb, loads
import numpy as np
import os
import time
import pyrealsense2 as rs
import datetime


class Mythread1(QThread):
    # this thread used to handle the eyeball tracker
    photeSignal = pyqtSignal(QPixmap)
    d = pyqtSignal(str)

    def __init__(self, file_path):
        super(Mythread1, self).__init__()
        self.context = zmq.Context()
        # open a req port to talk to pupil
        self.addr = "127.0.0.1"  # remote ip or localhost
        self.req_port = "50020"  # same as in the pupil remote gui
        self.req = self.context.socket(zmq.REQ)  # 设置socket类型，请求端
        self.req.connect("tcp://{}:{}".format(self.addr, self.req_port))  # 服务端为eyetracker，默认使用本地端口50020
        # ask for the sub port
        self.req.send_string("SUB_PORT")  # Request 'SUB_PORT' for reading data
        self.sub_port = self.req.recv_string()
        # open a sub port to listen to pupil
        self.sub = self.context.socket(zmq.SUB)
        self.sub.connect("tcp://{}:{}".format(self.addr, self.sub_port))

        #################### GAZE ####################

        self.context2 = zmq.Context()
        # open a req port to talk to pupil

        self.req2 = self.context2.socket(zmq.REQ)
        self.req2.connect("tcp://{}:{}".format(self.addr, self.req_port))
        # ask for the sub port
        self.req2.send_string("SUB_PORT")
        self.sub_port2 = self.req2.recv_string()
        print("sub_port2:", self.sub_port2)

        # open a sub port to listen to pupil
        self.sub2 = self.context2.socket(zmq.SUB)
        self.sub2.connect("tcp://{}:{}".format(self.addr, self.sub_port))

        # set subscriptions to topics
        # recv just pupil/gaze/notifications
        # sub.setsockopt_string(zmq.SUBSCRIBE, "pupil.")
        self.sub2.setsockopt_string(zmq.SUBSCRIBE, 'gaze')

        ####################  GAZE ####################

        # set subscriptions to topics
        # recv just pupil/gaze/notifications
        self.sub.setsockopt_string(zmq.SUBSCRIBE, "frame.")
        self.recent_world = None
        self.FRAME_FORMAT = "bgr"
        self.notification = {"subject": "frame_publishing.set_format", "format": self.FRAME_FORMAT}
        self.notify()
        self.show = None
        self.showImage = None
        # self.cap = cv2.VideoCapture(2)
        # self.cap.set(5, 60)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # self.videoWrite = cv2.VideoWriter(r'C:\Users\90335\Desktop\2\test.mp4', self.fourcc, 30,
        #                                   (960,600))
        self.num = 0  # counter for the photo
        self.file_name = self.get_time()[:10]
        # self.root_path = r"E:\data\eyetracker"
        # self.file_path = os.path.join(self.root_path, self.file_name) # create a file storage based on the time
        # self.file_exist(self.file_path) # please refer to the code below
        self.file_path = file_path
        self.video_name = "1.mp4"
        self.video_path = os.path.join(self.file_path, self.video_name)
        self.videoWrite = cv2.VideoWriter(self.video_path, self.fourcc, 60,
                                          (960, 539))
        self.eyetracker_txt_name = "1.txt"
        self.time_txt_name = "time.txt"
        self.txt_path = os.path.join(self.file_path, self.eyetracker_txt_name)
        self.time_txt_path = os.path.join(self.file_path, self.time_txt_name)

    def get_time(self):
        now = time.localtime()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
        return now_time

    def file_exist(self, file_path):  # check does the file exsist or not
        if not os.path.exists(file_path):
            print("do not exists")
            os.makedirs(file_path)
        else:
            print("exist")

    def notify(self):
        """Sends ``notification`` to Pupil Remote"""
        self.topic = "notify." + self.notification["subject"]
        self.payload = packb(self.notification, use_bin_type=True)
        self.req.send_string(self.topic, flags=zmq.SNDMORE)
        self.req.send(self.payload)
        return self.req.recv_string()

    def has_new_data_available(self):  #
        # Returns True as long subscription socket has received data queued for processing
        return self.sub.get(zmq.EVENTS) & zmq.POLLIN

    def has_new_data_available2(self):  #
        # Returns True as long subscription socket has received data queued for processing
        return self.sub2.get(zmq.EVENTS) & zmq.POLLIN

    def recv_from_sub(self):  #
        """Recv a message with topic, payload.
        Topic is a utf-8 encoded string. Returned as unicode object.
        Payload is a msgpack serialized dict. Returned as a python dict.
        Any addional message frames will be added as a list
        in the payload dict with key: '__raw_data__' .
        """
        topic = self.sub.recv_string()
        payload = unpackb(self.sub.recv(), raw=False)
        extra_frames = []
        while self.sub.get(zmq.RCVMORE):
            extra_frames.append(self.sub.recv())
        if extra_frames:
            payload["__raw_data__"] = extra_frames
        return topic, payload

    def run(self):
        with open(file=self.time_txt_path, mode="w") as f1:  # write down the abs time
            f1.write("date time\n")
            with open(file=self.txt_path, mode="w") as f:  # write down the position of the gaze
                while 1:
                    # ref, self.frame = self.cap.read()
                    # Save the video file if the user want to stop
                    if QThread.currentThread().isInterruptionRequested():
                        # self.cap.release()
                        self.videoWrite.release()
                        self.d.emit("finished")
                        break
                    # Ensure we get all the data that we need from the socket
                    while self.has_new_data_available() & self.has_new_data_available2():
                        topic, msg = self.recv_from_sub()
                        if topic.startswith("frame.") and msg["format"] != self.FRAME_FORMAT:
                            print(
                                f"different frame format ({msg['format']}); "
                                f"skipping frame from {topic}"
                            )
                            continue
                        if topic == "frame.world":  # get the video data from the first angle
                            self.recent_world = np.frombuffer(
                                msg["__raw_data__"][0], dtype=np.uint8
                            ).reshape(msg["height"], msg["width"], 3)
                    if (self.recent_world is not None):
                        # print(self.num)
                        self.num += 1  # count the photo that we collected
                        # if self.num % 2 ==0:
                        #     self.videoWrite.write(self.recent_world)
                        topic2 = self.sub2.recv_string()

                        msg2 = self.sub2.recv()

                        msg2 = loads(msg2, raw=False)

                        point_x = max(0, msg2['norm_pos'][0])
                        point_y = max(0, msg2['norm_pos'][1])
                        circle_x = point_x * self.recent_world.shape[1]
                        circle_y = self.recent_world.shape[0] - point_y * self.recent_world.shape[0]
                        # cv2.circle(self.recent_world, (int(circle_x), int(circle_y)), 10, (0, 0, 255), 5)
                        ##################################################
                        self.show = cv2.resize(self.recent_world, (960, 539))  # 把读到的帧的大小重新设置为 640x480
                        if True:  # reduce the size of the video file by half because the frame rate is too high
                            self.videoWrite.write(self.show)
                            txt_x = point_x * 960
                            txt_y = 539 - point_y * 539
                            line = str(int(txt_x)) + " " + str(int(txt_y)) + "\n"
                            f.write(line)
                            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "\n"
                            f1.write(now_time)
                        self.show = cv2.cvtColor(self.show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色

                        self.showImage = QImage(self.show.data, self.show.shape[1], self.show.shape[0],
                                                QImage.Format_RGB888)
                        self.photeSignal.emit(QPixmap.fromImage(self.showImage))


class Camera(object):
    # realsense相机处理类

    def __init__(self, width=960, height=540, fps=60):
        self.width = width
        self.height = height
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, fps)
        self.pipeline.start(self.config)  # 开始连接相机

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()  # 获得frame (包括彩色，深度图)
        # 创建对齐对象
        align_to = rs.stream.color  # rs.align允许我们执行深度帧与其他帧的对齐
        align = rs.align(align_to)  # “align_to”是我们计划对齐深度帧的流类型。
        aligned_frames = align.process(frames)
        # 获取对齐的帧
        color_frame = aligned_frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        return color_image

    def release(self):
        self.pipeline.stop()


class Mythread2(QThread):  # handling the video data of the simple webcam
    photeSignal = pyqtSignal(QPixmap)
    d = pyqtSignal(str)

    def __init__(self, file_path):
        super(Mythread2, self).__init__()

        self.file_name = self.get_time()[:10]
        self.root_path = r"E:\data\realsense"
        # self.file_path = os.path.join(self.root_path,self.file_name)
        # self.file_exist(self.file_path)
        self.file_path = file_path
        # self.video_name = self.get_time()[-8:-6]+self.get_time()[-5:-3]+self.get_time()[-2:]+".mp4"
        self.video_name = "1.mp4"
        self.video_path = os.path.join(self.file_path, self.video_name)
        # 视频保存路径
        # 初始化参数
        self.fps, self.w, self.h = 60, 960, 540
        self.mp4 = cv2.VideoWriter_fourcc(*'mp4v')  # 视频格式
        self.wr = cv2.VideoWriter(self.video_path, self.mp4, self.fps, (self.w, self.h), isColor=True)  # 视频保存而建立对象
        self.cam = Camera(self.w, self.h, self.fps)
        # 保存绝对时间戳
        self.realsense_time_txt_name = "realsense_time.txt"
        self.realsense_txt_path = os.path.join(self.file_path, self.realsense_time_txt_name)

    def get_time(self):  # the same function as the previous one
        now = time.localtime()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
        return now_time

    def file_exist(self, file_path):  # the same function as the previous one
        if not os.path.exists(file_path):
            print("do not exists")
            os.makedirs(file_path)
        else:
            print("exist")

    def run(self):
        with open(file=self.realsense_txt_path, mode="w") as f2:
            while 1:
                color_image = self.cam.get_frame()
                # print(self.name)

                if QThread.currentThread().isInterruptionRequested():
                    # release all the resource if the user want to stop
                    self.wr.release()
                    self.cam.release()
                    self.d.emit("finished")
                    print("finish")
                    break
                if color_image is not None:
                    # path = r"C:\Users\90335\Desktop\1"
                    # pic_name = str(self.name) + ".png"
                    # new_path = os.path.join(path,pic_name)
                    # self.show = cv2.resize(self.frame, (960,600))  # 把读到的帧的大小重新设置为 640x480
                    self.wr.write(color_image)
                    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "\n"
                    f2.write(now_time)
                    color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色

                    self.showImage = QImage(color_image, color_image.shape[1], color_image.shape[0],
                                            QImage.Format_RGB888)
                    self.photeSignal.emit(QPixmap.fromImage(self.showImage))
                else:
                    self.cap = cv2.VideoCapture("1.mp4")


class MainWindow(QWidget, Ui_Form):  # handling the UI issue
    def __init__(self):
        # 继承(QMainWindow,Ui_MainWindow)父类的属性
        super(MainWindow, self).__init__()
        # 初始化界面组件
        self.setupUi(self)
        self.status = 0
        self.pushButton.clicked.connect(self.test)
        self.comboBox.activated[str].connect(self.onActivated)
        self.athlete_name = "Leung Yuk Wing"
        self.eyetracker_path = None
        self.realsense_path = None

    def onActivated(self, text):
        self.athlete_name = text

    def creat_file(self):
        root_path = "./data"
        self.file_exist(root_path)
        root_date_file_name = self.get_time()[:10]
        root_date_file_path = os.path.join(root_path, root_date_file_name)
        self.file_exist(root_date_file_path)

        athlete_list = os.listdir(root_date_file_path)
        num_athelte = 0
        for name in athlete_list:
            if self.athlete_name == name[:-4]:
                num_athelte += 1
        athlete_file_name = self.athlete_name + "_" + ("%03d" % (num_athelte + 1))
        athlete_file_path = os.path.join(root_date_file_path, athlete_file_name)
        self.file_exist(athlete_file_path)
        self.realsense_path = os.path.join(athlete_file_path, "realsense")
        self.eyetracker_path = os.path.join(athlete_file_path, "eyetracker")
        self.file_exist(self.realsense_path)
        self.file_exist(self.eyetracker_path)

    def get_time(self):
        now = time.localtime()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
        return now_time

    def file_exist(self, file_path):  # check is the file exist or not
        if not os.path.exists(file_path):
            print(file_path, " is not exists")
            os.makedirs(file_path)
        else:
            print(file_path, " is exists")
            pass

    def test(self):
        if self.status == 0:
            self.creat_file()
            self.my_train = Mythread1(self.eyetracker_path)  # create the thread for the eyeball tracker
            self.my_train.photeSignal.connect(self.showPic1)
            self.my_train.d.connect(self.hideAll)
            self.my_train.start()

            self.status = 1  # indicate the thread is running
            self.pushButton.setText("Stop")
            # self.limit_frame_2()
        else:
            try:
                if self.my_train.isRunning():  # check the thread is running properly or not
                    self.my_train.requestInterruption()
                    self.my_train.quit()
                    self.my_train.wait()
            except:
                pass  # It can be done usually, so just pass

            self.pushButton.setText("Start")
            self.status = 0  # update the state

    def limit_frame_1(self):
        count = 0
        while True:
            count += 1
            if count >= 10000:
                try:
                    if self.my_train.isRunning():  # check the thread is running properly or not
                        self.my_train.requestInterruption()
                        self.my_train.quit()
                        self.my_train.wait()
                except:
                    print("Error happened when start collecting")
                    pass  # It can be done usually, so just pass
                try:
                    if self.my_train2.isRunning():
                        self.my_train2.requestInterruption()
                        self.my_train2.quit()
                        self.my_train2.wait()
                except:
                    pass  # It can be done usually, so just pass
                self.pushButton.setText("Start")
                self.status = 0  # update the state
                break

    def limit_frame_2(self):
        count = 0
        while True:
            count += 1
            if count >= 10000:
                try:
                    if self.my_train.isRunning():  # check the thread is running properly or not
                        self.my_train.requestInterruption()
                        self.my_train.quit()
                        self.my_train.wait()
                except:
                    pass  # It can be done usually, so just pass
                self.pushButton.setText("Start")
                self.status = 0  # update the state
                break

    def showPic1(self, qImg):  # reveral the video data on screen 1
        self.image_label.setPixmap(qImg)

    def showPic2(self, qImg):  # reveral the video data on screen 2
        self.image_label_2.setPixmap(qImg)

    def hideAll(self):
        self.image_label.clear()
        self.image_label_2.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 实例化界面
    window = MainWindow()
    # 显示界面
    window.show()
    # 阻塞，固定写法
    sys.exit(app.exec_())
