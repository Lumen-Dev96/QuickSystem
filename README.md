# Quick System

This template should help get you collecting [eyetracker](https://docs.pupil-labs.com/core/developer/), pendo handwriting, [realsense camera](https://github.com/IntelRealSense/librealsense) data.

## Enviroment

+ python >= 3.9

```
conda create --name QuickSystem python=3.9
```

### Install CUDA

use ` nvidia-smi` to check which CUDA version you need to download:

https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html

### Install cuDNN

https://developer.nvidia.com/rdp/cudnn-archive

### Install Pytorh

you can find your version according to this [reference](https://pytorch.org/), eg:

```
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

after installation, you can run `test_cuda.py` to check if you install all the staff above successfully

## Project Setup

```sh
pip install ultralytics
pip install msgpack pyzmq pyqt5 pyrealsense2
```

### Compile Pyqt5

```sh
 pyuic5 -o .\Boccia_UI.py .\Boccia_UI.ui
```

