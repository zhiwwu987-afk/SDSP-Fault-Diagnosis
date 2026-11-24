# SDSP: Standardized Data Splitting Protocol for Fault Diagnosis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Official repository for the paper: **"Temporal Leakage in Windowed Time-Series Classification: Systematic Evaluation Bias and a Standardized Splitting Protocol for Fault Diagnosis"**.

---

## 💡 Motivation & Background

With the rapid development of deep learning in continuous time-series analysis, high test accuracy is often regarded as strong evidence of a model's powerful detection and diagnostic capabilities. However, this conclusion holds **only if the test set is strictly blind and free from data leakage**. 

Currently, there is a lack of systematic research on how time-series data splitting methods affect the true performance of models. Using vibration-based fault diagnosis as a representative scenario, this study systematically investigates how random splitting of overlapping sliding windows leads to temporal data leakage, thereby causing an artificial inflation of apparent model performance.

To address this evaluation limitation, we propose the **Standardized Data Splitting Protocol (SDSP)**. By enforcing block-level temporal isolation and a safety gap ($$\Delta T$$), while preserving intra-set overlap for data augmentation, SDSP explicitly decouples evaluation integrity from sample expansion at the operational level. Furthermore, we introduce the **Leakage Impact Factor ($$LIF$$)** and **Generalization Deception Degree ($$\Delta Gap$$)** as supplementary metrics to quantify a model's vulnerability to temporal redundancy.

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

This project utilizes two distinct datasets. Please follow the instructions below to set them up correctly.

### 1. CWRU Bearing Dataset (Included)
For convenience, the required subset of the Case Western Reserve University (CWRU) dataset is **included directly in this repository**. 
- Location: `data/` (e.g., `data/0_0.mat`, `data/7_1.mat`, etc.)
- You can run `SDSP_CWRU_test.ipynb` immediately without additional data downloading.

### 2. UM-GearEcc Dataset (External Download Required)
Due to GitHub's file size limitations, the UM-GearEcc dataset is not included in this repository. 
To run the ECC experiments (`SDSP_ECC_test.ipynb`), please follow these steps:
1. Download the raw dataset from the official repository: [UM-GearEccDataset](https://github.com/LeeJMJM/UM-GearEccDataset).
2. Extract the downloaded files.
3. Place the required `.mat` files into the appropriate path as specified in the `SDSP_ECC_test.ipynb` notebook (e.g., `data/ECC/` or your custom local directory).

---

## 🚀 Quick Start

**1. Clone the repository:**
```bash
git clone https://github.com/your-username/SDSP-Fault-Diagnosis.git
cd SDSP-Fault-Diagnosis
