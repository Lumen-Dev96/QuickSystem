# Quick System

This template should help get you collecting [eyetracker](https://docs.pupil-labs.com/core/developer/), pendo handwriting, [realsense camera](https://github.com/IntelRealSense/librealsense) data.

## Enviroment

```
python >= 3.7
```

## Project Setup

```sh
pip install -r requirements.txt
```

### Compile Pyqt5

```sh
 pyuic5 -o .\Boccia_UI.py .\Boccia_UI.ui
```

### Import Data

```
/src/assets/ExcelProcess/Excel {id}/...
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
