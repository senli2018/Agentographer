#  Pulmonary nodule detection model in Agentographer



[[Paper]](https://arxiv.org/pdf/1711.08324v1.pdf)

## Model Overview

‌Pulmonary Nodule Detection Model‌ primarily utilizes the methodology from the paper "[Evaluate the Malignancy of Pulmonary Nodules Using the 3D Deep Leaky Noisy-or Network](https://arxiv.org/pdf/1711.08324v1.pdf)".
This paper proposes an ‌&zwnj;**automated lung cancer diagnosis system‌‌**&zwnj; based on a &zwnj;**‌3D deep neural network‌**&zwnj;, which significantly improves diagnostic accuracy by integrating two critical modules: ‌nodule detection‌ and ‌malignancy probability assessment‌. Key contributions include:
- &zwnj;**‌Dual-Module Architecture‌**&zwnj;:
  - &zwnj;**‌N-Net (Nodule Detector Network)**&zwnj;‌: A 3D region proposal network for detecting all suspicious pulmonary nodules in CT scans.
  - &zwnj;**‌C-Net (Case Classification Network)**&zwnj;‌: Evaluates malignancy probabilities of the Top5 nodules (filtered by detection confidence) and generates final diagnostic results by fusing global information via a ‌Leaky Noisy-or Network‌.
- &zwnj;**‌Shared Backbone Network‌**&zwnj;: An improved 3D U-Net serves as a shared feature extractor for both modules, reducing computational costs.
- &zwnj;**‌Alternating Training Strategy‌**&zwnj;: Mitigates overfitting issues caused by limited medical data.

‌Structure preserved with technical terms and emphasis retained.

## Model Architecture
### 1. N-Net 
- &zwnj;**Inputs**&zwnj;：3D volumetric data of lung CT scan. 
- &zwnj;**Outputs**&zwnj;：Coordinates and detection confidence of all suspicious nodules.  
- &zwnj;**technical realization**&zwnj;：Nodule localization and classification based on 3D Region Proposal Network (RPN).

### 2. C-Net 
- &zwnj;**输入**&zwnj;：N-Net输出的Top5结节区域  
- &zwnj;**Processing Pipeline**&zwnj;：  
1. Independently evaluate the malignancy probability of each nodule
2. Through &zwnj;**Leaky Noisy or Layer**&zwnj; Integrate multiple nodule information and calculate the overall cancer probability of the patient.
3. Introduce a leakage factor to address the issue of false negatives and enhance the robustness of the model.

### 3. Backbone
- &zwnj;**基础结构**&zwnj;：Improved 3D U-Net, supporting end-to-end feature learning. 
- &zwnj;**优化目标**&zwnj;：Joint loss function for nodule detection and malignant assessment.



## Installation

```bash
### environment
- python 3.12,
- CUDA 8.0, 
- cudnn 5.1, 
- h5py (2.6.0), 
- SimpleITK (0.10.0), 
- numpy (1.11.3), 
- nvidia-ml-py (7.352.0), 
- matplotlib (2.0.0), 
- scikit-image (0.12.3), 
- scipy (0.18.1), 
- pyparsing (2.1.4), 
- pytorch (0.1.10+ac9245a)
```

To install with pip, the commands are very similar, but you will have to manage your own environment and make sure to install fairseq2 manually first. 

```bash
pip install --upgrade pip
pip install torch==2.5.1 --extra-index-url https://download.pytorch.org/whl/cu121 --upgrade
pip install -r requirements.txt
```

## Usage

### Preparing data

All data are resized to 1x1x1 mm, the luminance is clipped between -1200 and 600, scaled to 0-255 and converted to uint8. A mask that include the lungs is calculated, luminance of every pixel outside the mask is set to 170. The results will be stored in 'preprocess_result_path' defined in config_training.py along with their corresponding detection labels.

### Downloading data
Downloading the model parameters from  [Google Drive](https://drive.google.com/drive/folders/1XEAUf1dyZ07VdcRg4HpRgGWkLhMkPGeu?usp=drive_link),
and place it in \AI-Driven-Diagnosis\model folder.

Prepare stage1 data, LUNA data, and LUNA segment results (https://luna16.grand-challenge.org/download/), unzip them to separate folders

### Evaluating models
**Step 1.** Repare stage1 data, LUNA data, and LUNA segment results 

**Step 2.** go to root folder

**Step 3.** open config_submit.py, filling in datapath with the stage 2 data path

**Step 4.** run inference.py
```bash
cd lung_nod
python inference.py
```
## Usage in Agentographer

### The function lung_node(image: UploadFile=File(None)) in  inference.py is the API service for Agentographer.