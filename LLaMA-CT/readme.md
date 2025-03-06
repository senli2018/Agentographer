# LLaMA_CT in Agentographer

This repository provides the official implementations and experiments for LLaMA_CT.

The file structure of this repository is as follows.
``` 
LLaMA-CT  
├── LLaMA-Factory  
│   └── examples  
│       └── inference  
│           └── llama3_lora_sft.yaml        # API configuration file, specifying model_path and adapter_path  
└── test  
    ├── test.py                     # Script for testing model outputs  
    ├── benchmark.py                # Evaluation script for ROUGE-L, METEOR, CIDEr  
    ├── test_results.json           # Generated test result file of ours
    └── LLaMA_CT_test_data_demo     # Includes demo test files
```
### Downloading data
Downloading the model parameters from  [Google Drive](https://drive.google.com/drive/folders/1oRfQWCsUCWiGNdizdLshAfYsOEUA3Til?usp=drive_link),
and place them in \LLaMA-CT path.

## Reproduce our results

```
conda create -n llama-ct python==3.10
cd LLaMA-CT/LLaMA-Factory
pip install -e ".[torch,metrics]"
```

Modify the ``` model_name_or_path``` and ``` adapter_name_or_path``` in the LLaMA-CT/LLaMA-Factory/examples/inference/llama3_lora_sft.yaml file to the paths of the base model and adapter weight files you downloaded.

Use the following command to launch the model API.

``` 
API_PORT=8000 llamafactory-cli api examples/inference/llama3_lora_sft.yaml
```

Then, open a new terminal window, navigate to the **test** folder, and modify the relevant file paths in **test.py**. 

Use ``` python test.py ``` to obtain the test result file of **LLaMA-CT**.

Modify **test_results.json** in **benchmark.py** to the result file of **LLaMA-CT** you just obtained.

Use ``` python benchmark.py ```  to obtain our **ROUGE-L**, **METEOR**, and **CIDEr** scores.


#补充开放接口的描述
