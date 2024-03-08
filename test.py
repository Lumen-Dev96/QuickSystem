from ctypes import *
import time

dll = CDLL("./SDK/x64/DigitNoteUSBController.dll")

print(dll.connectDevice())

print(dll.switchToRealTimeMode())

CallbackFunc = CFUNCTYPE(None, c_int, c_int, c_int)

def OnProgressCallbackForRealTimePenDatas(x, y, pressure):
    print("Received real-time pen data: x={}, y={}, pressure={}".format(x, y, pressure))

c_callback_func = CallbackFunc(OnProgressCallbackForRealTimePenDatas)

dll.SetCallBackForRealTimePenDatas(c_callback_func)

while True:
    time.sleep(1)