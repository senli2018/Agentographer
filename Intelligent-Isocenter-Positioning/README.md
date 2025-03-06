#  AI(title)
## human pose estimator

## Model Overview

The human pose estimator is mainly implemented using the mmpose framework.MMPose is an open-source toolbox for pose estimation based on PyTorch.

It is a part of the [OpenMMLab project](https://github.com/open-mmlab).

The main branch works with **PyTorch 1.8+**.

This project implements a YOLOX-based human pose estimator, utilizing the approach outlined in YOLO-Pose: Enhancing YOLO for Multi Person Pose Estimation Using Object Keypoint Similarity Loss (CVPRW 2022). This pose estimator is lightweight and quick, making it well-suited for crowded scenes.

Key contributions include:
- &zwnj;**Load YOLOX-Pose model in mmpose**&zwnj;: Measure the key point information of the human body on the CT machine.
- &zwnj;**Human body reconstruction based on depth camera**&zwnj;: Add depth information to the calculated two-dimensional keypoints using a depth camera to form a three-dimensional lattice; Build a human body model based on a three-dimensional lattice.
- &zwnj;**Post processing of attitude key points**&zwnj;: Used for obtaining different patient conditions based on the three-dimensional human body reconstruction of the patient, and flexibly adjusting the CT machine's bed entry distance and bed height information.

## Model Architecture
### 1. YOLOX-Pose
- &zwnj;**Input**&zwnj;: 2D image of the human body lying on a CT machine.
- &zwnj;**Output**&zwnj;: Key point information of the human body.  
- &zwnj;**Processing Pipeline**&zwnj;:  
  1. Using collection devices to capture 2D human body images.
  2. Preprocessing, including normalization, removal of some useless areas, focusing on human body position, etc
  3. Input the image into the model to obtain keypoint results.


### 2. Depth camera human body modeling
- &zwnj;**Input**&zwnj;: Camera captures images.
- &zwnj;**Output**&zwnj;: Depth map, spherical map, and transformation matrix of the human body
- &zwnj;**Processing Pipeline**&zwnj;:  
  1. Constructing 3D reconstruction results of human body based on depth map and keypoint coordinates.
  2. Calculate the distance between the key points and the key points of the human body.
  3. Calculate the distance between key points and a three-dimensional plane

### 3. Post processing of attitude key points
- &zwnj;**Input**&zwnj;: Key point information, including key spatial coordinates.
- &zwnj;**Output**&zwnj;: Need to adjust bed height and bed entry distance
- &zwnj;**Processing Pipeline**&zwnj;:  
  1. Calculate the adjusted values based on the required key points.

### Downloading data
Downloading the model parameters from  [Google Drive](https://drive.google.com/drive/folders/1gPyYD104KWhDW7Fft2khp_eU22TlafKJ?usp=drive_link),
and place it in "\Intelligent-Isocenter-Positioning\mmpose" path.


## Installation
This environment helps you to train and test our DWPose. You can ignore the following installation for ControlNet.

You can refer [MMPose Installation](https://mmpose.readthedocs.io/en/latest/installation.html) or
```
# Set MMPose environment
pip install torch==1.9.1+cu111 torchvision==0.10.1+cu111 torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html
pip install -r requirements.txt
```
```
# Install RGB-D Camera environment
refered Azure Kinect SDK https://github.com/microsoft/Azure-Kinect-Sensor-SDK
```

## For YOLOX

### Prerequisites

- Python 3.7 or higher

- PyTorch 1.6 or higher

- [MMEngine](https://github.com/open-mmlab/mmengine) v0.6.0 or higher

- [MMCV](https://github.com/open-mmlab/mmcv) v2.0.0rc4 or higher

- [MMDetection](https://github.com/open-mmlab/mmdetection) v3.0.0rc6 or higher

- [MMYOLO](https://github.com/open-mmlab/mmyolo) <span style="color:red"> **v0.5.0**</span>

- [MMPose](https://github.com/open-mmlab/mmpose) v1.0.0rc1 or higher

All the commands below rely on the correct configuration of `PYTHONPATH`, which should point to the project's directory so that Python can locate the module files. **In `yolox-pose/` root directory**, run the following line to add the current directory to `PYTHONPATH`:

```shell
export PYTHONPATH=`pwd`:$PYTHONPATH
```

## Usage
### Downloading data
```bash
python download_test_data.py
```
### Evaluating models
#### 1. Test the mmpose model
The required parameters are the input image, mmpose parameter configuration, model parameters to be loaded, and output path --out-file.
```bash
python *.jpg mmpose/configs/wholebody_2d_keypoint/rtmpose/ubody/rtmpose-l_8xb32-270e_coco-ubody-wholebody-384x288.py  mmpose/dw-ll_ucoco_384.pth  --out-file vis_results.jpg
```
#### 2. Test calculation of human posture estimation method

**Step 1.** Manually fill in input_dir and file_name as the required path and file name, respectively.
**Step 2.** run inference.py
```bash
cd pose_estimator
python inference.py
```
#### 3. Test Depth camera algorithm
```bash
cd pose_estimator
python video_body_key_point_depth_distance_web.py
```