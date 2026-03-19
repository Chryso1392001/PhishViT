# 🛡️ PhishViT: Real-Time Phishing Detection Using Vision Transformers

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0-red)](https://pytorch.org)
[![Accuracy](https://img.shields.io/badge/Accuracy-96.91%25-green)]()
[![AUC-ROC](https://img.shields.io/badge/AUC--ROC-0.9974-green)]()

## Overview
PhishViT is a real-time phishing detection framework that operates on 
webpage screenshots using a fine-tuned DeiT-Small Vision Transformer.

## Results
| Metric    | V1 (253 imgs) | V2 (642 imgs) |
|-----------|--------------|--------------|
| Accuracy  | 78.95%       | **96.91%**   |
| Precision | 73.91%       | **95.92%**   |
| Recall    | 89.47%       | **97.92%**   |
| F1-Score  | 80.95%       | **96.91%**   |
| AUC-ROC   | 0.9363       | **0.9974**   |

## Architecture
- Model: DeiT-Small (22M parameters)
- Input: 224×224 webpage screenshots
- Training: Two-stage fine-tuning on Tesla T4 GPU
- Dataset: 642 balanced real-world screenshots

## Repository Structure
```
PhishViT/
├── PhishViT_Training.ipynb   # Main training notebook
├── data/                     # Dataset collection scripts
│   └── collect_urls.py
├── src/                      # Source code
│   ├── screenshot_capture.py
│   └── train.py
├── results/                  # Training curves & attention maps
└── README.md
```

## How to Run
1. Open PhishViT_Training.ipynb in Google Colab
2. Mount Google Drive
3. Run all cells in order

## Citation
If you use this work please cite:
```
@article{ndayisabye2026phishvit,
  title={PhishViT: Real-Time Visual Phishing Detection from 
         Webpage Screenshots Using Vision Transformers},
  author={Ndayisabye, Jean Chrysostome},
  institution={University of Rwanda},
  year={2026}
}
```

## Author
**Jean Chrysostome NDAYISABYE**  
University of Rwanda, College of Science and Technology  
Department of Information Systems
```

---

## Step 5 — Upload Your Other Files

On your GitHub repo page click **Add file → Upload files** and upload:
```
✅ src/collect_urls.py
✅ src/screenshot_capture_v2.py
✅ src/augment_data.py
✅ results/training_v2.png
✅ results/attention_v2.png
✅ models/  (optional — 83MB may be too large)
