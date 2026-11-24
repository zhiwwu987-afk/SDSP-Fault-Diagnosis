
# -*- coding: utf-8 -*-
"""
Strict Data Splitting Protocol (SDSP) for Rotating Machinery
==========================================================================

This module provides the official implementation of the SDSP framework,
including physically-informed temporal isolation and leakage-aware metrics.

Features:
    1. Auto-calculation of Safety Gap based on physical kinematics.
    2. Block-Holdout splitting with strict temporal isolation.
    3. Leakage-aware evaluation metrics (LIF & Delta Gap).

Citation:
---------
If you use this code or the SDSP protocol in your research, please cite:

Title: Temporal Leakage in Windowed Time-Series Classification: Systematic 
       Evaluation Bias and a Standardized Splitting Protocol for Fault Diagnosis
==========================================================================
"""


import math
import numpy as np

def calculate_safety_gap(rpm, sampling_rate, min_rotations=1.0):
    """
    Calculate the physically-informed safety gap based on rotational speed.
    
    Parameters:
    -----------
    rpm : float
        Rotational speed of the equipment (r/min).
    sampling_rate : int
        Sampling frequency (Hz).
    min_rotations : float, optional
        Minimum number of rotation periods for the gap (default is 1.0).
        
    Returns:
    --------
    gap_samples : int
        The safety gap in number of sample points.
    gap_seconds : float
        The safety gap in seconds.
    """
    if rpm <= 0:
        raise ValueError("RPM must be greater than 0.")
        
    # T_r = 60 / n (Rotation period in seconds)
    rotation_period = 60.0 / rpm
    
    # Delta T >= T_r
    gap_seconds = min_rotations * rotation_period
    
    # N_{Delta T} = ceil(Delta T * f_s)
    gap_samples = math.ceil(gap_seconds * sampling_rate)
    
    return gap_samples, gap_seconds


def sdsp_split(y, starts, rpm, sampling_rate, ratios=(0.7, 0.2, 0.1), window_length=2048, seed=42):
    """
    Perform SDSP Block-Holdout splitting with temporal isolation.
    
    Parameters:
    -----------
    y : np.ndarray
        Array of labels for each sample window.
    starts : np.ndarray
        Array of starting time indices (sample points) for each window.
    rpm : float
        Rotational speed (r/min) for gap calculation.
    sampling_rate : int
        Sampling frequency (Hz).
    ratios : tuple
        (Train, Validation, Test) split ratios.
    window_length : int
        Number of points in each sample window.
    seed : int
        Random seed for reproducibility.
        
    Returns:
    --------
    idx_tr, idx_va, idx_te : np.ndarray
        Indices for training, validation, and testing sets.
    """
    gap_samples, _ = calculate_safety_gap(rpm, sampling_rate)
    rng = np.random.RandomState(seed)
    
    train_r, val_r, test_r = ratios
    idx_tr, idx_va, idx_te = [], [], []
    
    for c in np.unique(y):
        cls_idx = np.where(y == c)[0]
        # Sort by actual temporal order
        cls_idx = cls_idx[np.argsort(starts[cls_idx])]
        
        n = len(cls_idx)
        n_tr = int(n * train_r)
        n_va = int(n * val_r)
        
        tr = cls_idx[:n_tr]
        va = cls_idx[n_tr:n_tr+n_va]
        te = cls_idx[n_tr+n_va:]

        if len(tr) and len(te):
            # Apply Safety Gap between Train and Validation
            tr_end_t = starts[tr].max() + window_length
            va = va[starts[va] >= tr_end_t + gap_samples] if len(va) else va
            
            # Apply Safety Gap between Validation and Test
            va_end_t = starts[va].max() + window_length if len(va) else tr_end_t
            te = te[starts[te] >= va_end_t + gap_samples]

        idx_tr.append(tr)
        idx_va.append(va)
        idx_te.append(te)
        
    return np.concatenate(idx_tr), np.concatenate(idx_va), np.concatenate(idx_te)


def calculate_leakage_metrics(acc_random_tr, acc_random_te, acc_sdsp_tr, acc_sdsp_te):
    """
    Calculate Leakage Impact Factor (LIF) and Generalization Deception Degree (Delta Gap).
    
    Parameters:
    -----------
    acc_random_tr, acc_random_te : float
        Train and Test accuracy under traditional Random Split.
    acc_sdsp_tr, acc_sdsp_te : float
        Train and Test accuracy under SDSP.
        
    Returns:
    --------
    lif : float
        Leakage Impact Factor (percentage).
    delta_gap : float
        Generalization Deception Degree.
    """
    # LIF = (Acc_Random - Acc_SDSP) / Acc_Random * 100%
    if acc_random_te == 0:
        lif = 0.0
    else:
        lif = ((acc_random_te - acc_sdsp_te) / acc_random_te) * 100.0
        
    # Delta Gap = |(Acc_tr - Acc_te)_SDSP - (Acc_tr - Acc_te)_Random|
    gap_sdsp = acc_sdsp_tr - acc_sdsp_te
    gap_random = acc_random_tr - acc_random_te
    delta_gap = abs(gap_sdsp - gap_random)
    
    return lif, delta_gap

# ==========================================================================
# Example Usage
# ==========================================================================
if __name__ == "__main__":
    # Example: Equipment running at 600 RPM, sampled at 51.2 kHz
    RPM = 600
    FS = 51200
    
    gap_pts, gap_sec = calculate_safety_gap(RPM, FS)
    print(f"Calculated Safety Gap: {gap_sec:.4f} seconds ({gap_pts} points)")
    
    # Example Metric Calculation
    lif, d_gap = calculate_leakage_metrics(
        acc_random_tr=0.99, acc_random_te=0.98, 
        acc_sdsp_tr=0.95, acc_sdsp_te=0.82
    )
    print(f"Leakage Impact Factor (LIF): {lif:.2f}%")
    print(f"Generalization Deception Degree (ΔGap): {d_gap:.4f}")
