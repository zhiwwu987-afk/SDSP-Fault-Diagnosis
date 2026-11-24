# SDSP: Standardized Data Splitting Protocol for Fault Diagnosis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Official repository for the paper: **"Temporal Leakage in Windowed Time-Series Classification: Systematic Evaluation Bias and a Standardized Splitting Protocol for Fault Diagnosis"**.

---

## 💡 Motivation & Background

With the rapid development of deep learning in continuous time-series analysis, high test accuracy is often regarded as strong evidence of a model's powerful detection and diagnostic capabilities. However, this conclusion holds **only if the test set is strictly blind and free from data leakage**. 

Currently, there is a lack of systematic research on how time-series data splitting methods affect the true performance of models. Using vibration-based fault diagnosis as a representative scenario, this study systematically investigates how random splitting of overlapping sliding windows leads to temporal data leakage, thereby causing an artificial inflation of apparent model performance.
<img width="758" height="397" alt="image" src="https://github.com/user-attachments/assets/52bdfda9-6bcd-424d-bafb-ea66f3396992" />

To address this evaluation limitation, we propose the **Standardized Data Splitting Protocol (SDSP)**. By enforcing block-level temporal isolation and a safety gap ($$\Delta T$$), while preserving intra-set overlap for data augmentation, SDSP explicitly decouples evaluation integrity from sample expansion at the operational level. 

## ✨ Key Highlights

- **SDSP Framework**: A plug-and-play data splitting protocol that guarantees zero temporal leakage across training, validation, and test sets.
- **Quantitative Metrics**: Introduces the Leakage Impact Factor ($$LIF$$) and Generalization Deception Degree ($$\Delta Gap$$) as supplementary metrics to quantify a model's vulnerability to temporal redundancy.
- **Model-Agnostic**: The core implementation (`sdsp_protocol.py`) is fully decoupled from specific deep learning architectures and can be easily adapted to other time-series tasks.
<img width="636" height="530" alt="image" src="https://github.com/user-attachments/assets/2d9181f1-234b-4e9f-8fbc-70f1a1ef8b97" />

---

## 📂 Repository Structure

The repository is organized to ensure out-of-the-box reproducibility for our experiments.

| File / Directory | Description |
|------------------|-------------|
| `sdsp_protocol.py` | **Core Implementation:** The independent, reusable SDSP module. |
| `SDSP_CWRU_test.ipynb` | **Experiment:** Jupyter Notebook for reproducing CWRU dataset results. |
| `SDSP_ECC_test.ipynb` | **Experiment:** Jupyter Notebook for reproducing UM-GearEcc dataset results. |
| `data/` | **Datasets:** Directory containing the required `.mat` data files. |

---

## 📊 Datasets & Preparation

This project utilizes two distinct datasets. Each raw signal file is truncated to **119,808 data points** to ensure consistent evaluation. Please follow the instructions below to set them up correctly.

### 1. CWRU Bearing Dataset (Included)
For convenience, the required subset of the Case Western Reserve University (CWRU) dataset (sampled at 12 kHz) is **included directly in this repository**. 
- Location: `data/` (e.g., `data/0_0.mat`, `data/7_1.mat`, etc.)
- You can run `SDSP_CWRU_test.ipynb` immediately without additional data downloading.

### 2. UM-GearEcc Dataset (External Download Required)
Due to GitHub's file size limitations, the UM-GearEcc dataset (sampled at 51.2 kHz) is not included in this repository. 
To run the ECC experiments (`SDSP_ECC_test.ipynb`), please follow these steps:
1. Download the raw dataset from the official repository: [UM-GearEccDataset](https://github.com/LeeJMJM/UM-GearEccDataset).
2. Extract the downloaded files.
3. Place the required `.mat` files into the appropriate path as specified in the `SDSP_ECC_test.ipynb` notebook (e.g., `data/ECC/` or your custom local directory).

---

## 🚀 Quick Start

**1. Clone the repository:**
```bash
git clone https://github.com/zhiwwu987-afk/SDSP-Fault-Diagnosis.git
cd SDSP-Fault-Diagnosis
---

2. Use the SDSP module in your own project:
You can easily import and apply our protocol to your own time-series tasks to ensure a strict and fair evaluation:

from sdsp_protocol import sdsp_split

# Example usage (refer to the source code for detailed parameters)
train_idx, val_idx, test_idx = sdsp_split(
    data_length=119808,
    window_size=2048,
    overlap_ratio=0.75,
    safety_gap=0.05, # \Delta T in seconds
    sampling_rate=51200
)
---

📝 Citation
If you find our protocol, code, or evaluation metrics (LIF, ΔGap) helpful in your research, please cite our paper:

@article{
  title={Temporal Leakage in Windowed Time-Series Classification: Systematic Evaluation Bias and a Standardized Splitting Protocol for Fault Diagnosis}
}

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.


