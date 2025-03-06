#  AI(title)
## lung segmentation

[[Paper]](https://arxiv.org/pdf/1711.08324v1.pdf)

## Model Overview

The pulmonary nodule segmentation model mainly uses data from the paper"[SAM 2: Segment Anything in Images and Videos](https://ai.meta.com/research/publications/sam-2-segment-anything-in-images-and-videos/)"。

Segment Anything Model 2 (SAM 2) is a foundation model towards solving promptable visual segmentation in images and videos. We extend SAM to video by considering images as a video with a single frame. 

Key contributions include:
- &zwnj;**Lung X-ray preprocessing and prompt coordinate point acquisition**&zwnj;: Used for preprocessing lung X-rays and obtaining prompt coordinate points for SAM2.
- &zwnj;**SAM2 network prediction**&zwnj;: Use SAM2 network for lung cavity segmentation.

## Model Architecture
### 1. Chest X-ray Preprocessing  
- &zwnj;**Input**&zwnj;: Raw 2D chest X-ray DICOM data.  
- &zwnj;**Output**&zwnj;: Processed DICOM data in PNG format.  
- &zwnj;**Processing Pipeline**&zwnj;:  
  1. Apply lung window normalization to DICOM format.
  2. Enhance image contrast for clearer anatomical boundaries.

### 2. SAM2 Model Prompt Coordinate Acquisition  
- &zwnj;**Input**&zwnj;: Preprocessed chest X-ray data.  
- &zwnj;**Output**&zwnj;: Keypoint coordinates of bilateral lung fields.  
- &zwnj;**Processing Pipeline**&zwnj;:  
  1. Perform lung field coarse segmentation using thresholding algorithm.
  2. Calculate Distance Map from coarse segmentation results.
  3. Generate keypoint coordinates using Distance Map and lung window parameters. 

### 3. SAM2 Model Prediction  
- &zwnj;**Input**&zwnj;: Keypoint coordinates of lung fields.  
- &zwnj;**Output**&zwnj;: Binary refined mask of lung fields.  
- &zwnj;**Processing Pipeline**&zwnj;:  
  1. Load pre-trained SAM2 network.
  2. Predict fine lung field masks using keypoints as spatial prompts.  
  
## Installation
SAM 2 needs to be installed first before use. The code requires python>=3.10, as well as torch>=2.5.1 and torchvision>=0.20.1. Please follow the instructions here to install both PyTorch and TorchVision dependencies. You can install SAM 2 on a GPU machine using:

SAM 2 needs to be installed first before use. The code requires `python>=3.10`, as well as `torch>=2.5.1` and `torchvision>=0.20.1`. Please follow the instructions [here](https://pytorch.org/get-started/locally/) to install both PyTorch and TorchVision dependencies. You can install SAM 2 on a GPU machine using:

```bash
git clone https://github.com/facebookresearch/sam2.git && cd sam2

pip install -e .
```
If you are installing on Windows, it's strongly recommended to use [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install) with Ubuntu.

To use the SAM 2 predictor and run the example notebooks, `jupyter` and `matplotlib` are required and can be installed by:

```bash
pip install -e ".[notebooks]"
```

## Usage

### Preparing data

Use the CT positioning film collected by the collector

### Downloading data
Downloading the model parameters from  [Google Drive](https://drive.google.com/drive/folders/1aGoijDIQnGI8p3nJlryWo04LtLacIcPG?usp=drive_link),
and place them in \CT-Scan-Range-Determination\checkpoints path.


### Evaluating models
#### Model Testing
**Step 1.** Enter the current directory
```bash
cd CT-Scan-Range-Determination
```
**Step 2.** Placed in the corresponding directory. 

    checkpoint: the model path
    model_cfg: the model configuration

**Step 3.** Execute script mask_interactivate.py
```bash
run mask_interactivate.py
```
#### API Testing
**Step 1.** Start the API using the above method and call it through a POST request.
```bash
cd lung_segmentation
uvicorn mask_interactivate:app --host 0.0.0.0 --port 7099 --log-level info
```

