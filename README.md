# Digital Twin ICU

**Machine Learning Models for Predicting Postoperative Complications**

[![GitHub Stars](https://img.shields.io/github/stars/paracelsus12-crypto/digital-twin-icu?style=social)](https://github.com/paracelsus12-crypto/digital-twin-icu)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://digital-twin-icu.streamlit.app)

---

## 🎯 Overview

**Digital Twin ICU** is a comprehensive machine learning system for predicting postoperative complications in surgical patients. The system contains **31 pre-trained Random Forest models** predicting major complications across **5 surgical specialties**:

- 🫀 **Cardiac Surgery** (7 models)
- 🏥 **Abdominal Surgery** (7 models)
- 🫁 **Thoracic Surgery** (6 models)
- 🩸 **Vascular Surgery** (6 models)
- 🦴 **Orthopedic Surgery** (6 models)

### Predicted Complications

**Universal Complications:**
- Acute Kidney Injury (AKI)
- Delirium
- Infection
- Respiratory Complications

**Specialty-Specific:**
- **Cardiac:** Atrial Fibrillation (AF), Low Cardiac Output (LCO), Stroke
- **Abdominal:** Anastomotic Leak, Ileus, VTE
- **Thoracic:** Air Leak, Atelectasis
- **Vascular:** Amputation, Thrombosis
- **Orthopedic:** Prosthetic Joint Infection (PJI), VTE

---

## 🚀 Quick Start

### Option 1: Web Application (Easiest)

Open the live Streamlit app:
**[https://digital-twin-icu.streamlit.app](https://digital-twin-icu.streamlit.app)**

No installation required! Upload patient data and get predictions in seconds.

### Option 2: Google Colab (No Setup)

Click to run in your browser:
- [Complete Version](https://colab.research.google.com/github/paracelsus12-crypto/digital-twin-icu/blob/main/google_colab/Complete.py)
- [Basic Version](https://colab.research.google.com/github/paracelsus12-crypto/digital-twin-icu/blob/main/google_colab/ICU_Digital_Twin.py)

### Option 3: Local Installation

```bash
# Clone repository
git clone https://github.com/paracelsus12-crypto/digital-twin-icu.git
cd digital-twin-icu

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run web_app/streamlit_app_full.py

# Open browser to http://localhost:8501
```

---

## 📊 Model Performance

### Cardiac Surgery Models
| Complication | Training AUC | External Validation AUC |
|---|---|---|
| Atrial Fibrillation (AF) | 0.935 | 0.72 |
| Acute Kidney Injury (AKI) | 0.925 | 0.68 |
| Delirium | 0.910 | 0.71 |
| Low Cardiac Output (LCO) | 0.920 | 0.69 |
| Infection | 0.913 | 0.65 |
| Respiratory | 0.925 | 0.73 |
| Stroke | 0.890 | 0.71 |

### Abdominal Surgery Models
| Complication | Training AUC | External Validation AUC |
|---|---|---|
| Anastomotic Leak | 0.940 | 0.61 |
| Acute Kidney Injury (AKI) | 0.914 | 0.58 |
| Ileus | 0.920 | 0.52 |
| Infection | 0.934 | 0.49 |
| Delirium | 0.919 | 0.69 |
| Respiratory | 0.907 | 0.55 |
| VTE | 0.928 | 0.63 |

### Thoracic Surgery Models
| Complication | Training AUC | External Validation AUC |
|---|---|---|
| Air Leak | 0.921 | 0.59 |
| Atelectasis | 0.928 | 0.64 |
| Acute Kidney Injury (AKI) | 0.925 | 0.59 |
| Delirium | 0.910 | 0.62 |
| Infection | 0.913 | 0.53 |
| Respiratory | 0.909 | 0.64 |

---

## 💾 Features & Input Data

### Required Patient Features (18-20 per surgery type)

**Demographics:**
- Age, Sex, BMI, Weight, Height

**Preoperative Labs:**
- Creatinine, Hemoglobin, Glucose, Albumin

**Comorbidities:**
- Diabetes, Hypertension, CKD Stage, COPD, Smoking Status

**Clinical:**
- ASA Class, Emergency Status, Surgery Duration

**Specialty-Specific:**
- FEV1% (Thoracic), VATS vs Open (Thoracic), Laparoscopic vs Open (Abdominal)

---

## 📚 Documentation

### For Users
- **[Installation Guide](docs/Installation_Guide.md)** - Step-by-step setup
- **[Hospital Integration](docs/Hospital_Integration.md)** - Integrate with EMR/EHR systems
- **[Clinical Examples](examples/)** - Real patient case studies
- **[Ukrainian Documentation](docs/README_UA.md)** - Документація українською мовою

### For Developers
- **[Model Architecture](docs/Model_Architecture.md)** - Technical details
- **[API Reference](src/)** - Python function documentation
- **[Jupyter Notebooks](notebooks/)** - Example code & analysis

### Academic
- **[BUS-18 Masterclass](docs/BUS-18_Masterclass.md)** - Educational materials
- **[Conference Presentation](presentations/)** - Slides & materials
- **[Clinical Case Studies](notebooks/05_Clinical_Cases.ipynb)** - Real patient scenarios

---

## 🔧 Usage Examples

### Example 1: Web App Interface
1. Visit [https://digital-twin-icu.streamlit.app](https://digital-twin-icu.streamlit.app)
2. Select surgery type (Cardiac, Abdominal, Thoracic, Vascular, Orthopedic)
3. Enter patient data
4. Get predictions for all relevant complications
5. View risk scores and visualizations

### Example 2: Python API

```python
from src.model_loader import load_model
from src.prediction import predict_complications
import pandas as pd

# Load model
model = load_model('cardiac', 'af')  # Cardiac AF model

# Prepare patient data
patient_data = pd.DataFrame({
    'age': [65],
    'sex': [1],  # 1=Male, 0=Female
    'bmi': [28],
    'creatinine': [0.9],
    'hemoglobin': [13.5],
    'glucose': [110],
    'albumin': [3.8],
    'diabetes': [0],
    'hypertension': [1],
    'asa_class': [3],
    'emergency': [0],
    'surgery_duration': [180],
    'copd': [0],
    'smoking': [0]
})

# Make prediction
risk_score = model.predict_proba(patient_data)[0][1]
print(f"AF Risk: {risk_score:.2%}")
```

### Example 3: Batch Predictions

```python
from src.prediction import predict_batch

# Load patient dataset
patients = pd.read_csv('patients.csv')

# Get predictions for all patients
results = predict_batch(patients, surgery_type='cardiac')

# Save results
results.to_csv('predictions.csv', index=False)
```

---

## 📁 Project Structure

```
digital-twin-icu/
├── README.md                          ← You are here
├── LICENSE                            (MIT License)
├── requirements.txt                   (Python dependencies)
│
├── web_app/
│   ├── streamlit_app_full.py         (Interactive web application)
│   ├── requirements.txt               (Streamlit dependencies)
│   └── config.json                    (Configuration)
│
├── models/
│   ├── cardiac/                       (7 cardiac models)
│   ├── abdominal/                     (7 abdominal models)
│   ├── thoracic/                      (6 thoracic models)
│   ├── vascular/                      (6 vascular models)
│   ├── orthopedic/                    (6 orthopedic models)
│   └── README.md                      (Model documentation)
│
├── data/
│   ├── training/                      (Training datasets)
│   │   ├── cardiac_training_data_v2.csv
│   │   ├── abdominal_training_data_v2.csv
│   │   └── ...
│   └── metrics/
│       └── all_surgery_metrics_v2.json
│
├── src/
│   ├── model_loader.py               (Load pre-trained models)
│   ├── prediction.py                 (Make predictions)
│   ├── data_preprocessing.py         (Prepare data)
│   ├── evaluation.py                 (Evaluate models)
│   └── utils.py                      (Helper functions)
│
├── notebooks/
│   ├── 01_Data_Exploration.ipynb
│   ├── 02_Model_Loading.ipynb
│   ├── 03_Making_Predictions.ipynb
│   ├── 04_Hospital_Integration.ipynb
│   └── 05_Clinical_Cases.ipynb
│
├── google_colab/
│   ├── Complete.py                   (Full Colab version)
│   ├── ICU_Digital_Twin.py           (Basic Colab version)
│   └── README.md
│
├── examples/
│   ├── cardiac_patient_example.json
│   ├── abdominal_patient_example.json
│   └── example_usage.py
│
├── presentations/
│   ├── BUS-18_Masterclass.pptx
│   ├── Digital_Twin_Overview_v1.pptx
│   └── Digital_Twin_Overview_v2.pptx
│
├── docs/
│   ├── README_UA.md                  (Українська документація)
│   ├── Installation_Guide.md
│   ├── Hospital_Integration.md
│   ├── Model_Architecture.md
│   ├── BUS-18_Masterclass.md
│
└── tests/
    ├── test_model_loading.py
    ├── test_predictions.py
    └── test_data_preprocessing.py
```

---

## 🏥 Clinical Integration

### Hospital EMR/EHR Integration

Digital Twin ICU can be integrated into hospital systems in multiple ways:

#### Option 1: Web App (Simplest)
- Hospital staff access Streamlit app via web browser
- No IT infrastructure needed
- No data stored locally
- [See integration guide](docs/Hospital_Integration.md)

#### Option 2: API Integration
- Custom API endpoint for hospital EHR
- Batch predictions for multiple patients
- Automated workflows
- [See API documentation](src/)

#### Option 3: Local Installation
- Install on hospital server
- Direct database integration
- HIPAA-compliant deployment
- [See installation guide](docs/Installation_Guide.md)

---

## 📖 Educational Materials

### For Medical Students & Residents

- **[BUS-18 Masterclass](docs/BUS-18_Masterclass.md)** - Complete educational curriculum
- **[Clinical Cases](notebooks/05_Clinical_Cases.ipynb)** - Real patient scenarios
- **[Case Testing](docs/Кейси_тест.md)** - Test your clinical judgment

### For Hospital Staff

- **[Hospital Integration](docs/Hospital_Integration.md)** - How to use in your hospital
- **[Implementation Guide](examples/)** - Step-by-step implementation
- **[FAQ & Troubleshooting](docs/FAQ.md)** - Common questions

### For Researchers

- **[Model Architecture](docs/Model_Architecture.md)** - Technical details
- **[Jupyter Notebooks](notebooks/)** - Data analysis & validation code

---

## 🔬 Research & Validation

### Research & Validation

**External Validation:**
- VitalDB Dataset: 6,388 surgical patients
- Mean AUC: 0.574 (Abdominal), 0.601 (Thoracic)
- Performance across 5 surgical specialties

**Conference Presentations & Educational Materials:**
- BUS-18 Conference (2026) - Masterclass materials
- Conference slides available in [presentations/](presentations/)
- Educational tutorials and clinical case studies in [notebooks/](notebooks/)

---

## 🌍 Citing This Work

If you use Digital Twin ICU in your research or clinical practice, please cite:

### BibTeX
```bibtex
@software{mazur2026digital,
  author = {Mazur, Andrii P.},
  title = {Digital Twin ICU: Machine Learning Prediction of Postoperative Complications},
  year = {2026},
  url = {https://github.com/paracelsus12-crypto/digital-twin-icu}
}
```

### APA
Mazur, A. P. (2026). Digital Twin ICU: Machine learning prediction of postoperative complications. *GitHub*. https://github.com/paracelsus12-crypto/digital-twin-icu

---

## 💬 Support & Community

### Questions & Issues
- **GitHub Issues**: [Report bugs or request features](https://github.com/paracelsus12-crypto/digital-twin-icu/issues)
- **GitHub Discussions**: [Q&A and general discussion](https://github.com/paracelsus12-crypto/digital-twin-icu/discussions)
- **Email**: paracelsus12@gmail.com

### Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

[See CONTRIBUTING.md](CONTRIBUTING.md) for more details.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

MIT License allows:
- ✅ Academic use
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ⚠️ Requires attribution

---

## 🙏 Acknowledgments

### Development
- Prof. Andrii P. Mazur, MD, PhD
- M.M. Amosov National Institute of Cardiovascular Surgery, Kyiv
- Department of Anesthesiology, Resuscitation and Extracorporeal Treatment Methods

### Data & Validation
- **VitalDB Dataset**: Seoul National University Hospital
- [Lee JS, et al. VitalDB: a high-fidelity multi-parameter vital signs database. Sci Data. 2019](https://github.com/vitaldb/vitaldb)

### Technical Stack
- **Python 3.8+**: [python.org](https://www.python.org)
- **scikit-learn**: [scikit-learn.org](https://scikit-learn.org)
- **Streamlit**: [streamlit.io](https://streamlit.io)
- **Pandas**: [pandas.pydata.org](https://pandas.pydata.org)

---

## 🔗 Related Resources

### Ukrainian Resources
- **[Virtual ICU Demo](https://github.com/paracelsus12-crypto/virtual-icu-demo)** - Related educational project

### External Links
- [M.M. Amosov National Institute of Cardiovascular Surgery](https://www.cardiac.kiev.ua)
- [Bogomolets National Medical University](https://www.nmu.ua)
- [ESAIC (European Society of Anaesthesiology and Intensive Care)](https://www.esaic.org)
- [BUS-18 Conference](https://anaesthesiaconference.kyiv.ua/)

---

## 📞 Contact

**Prof. Andrii P. Mazur, MD, PhD**
- Email: paracelsus12@gmail.com
- Institution: M.M. Amosov National Institute of Cardiovascular Surgery, Kyiv
- GitHub: [@paracelsus12-crypto](https://github.com/paracelsus12-crypto)

---

## ⭐ Support This Project

If you find Digital Twin ICU helpful, please:
- ⭐ **Star the repository** on GitHub
- 📢 **Share with colleagues** and friends
- 📝 **Cite in your research**
- 💬 **Provide feedback** via GitHub Issues
- 🤝 **Contribute improvements**

---

**Last Updated:** April 2026
**Version:** 1.0.0 (Initial Public Release)
**Status:** Active Development & Community Contributions Welcome 🚀

---

## 🎓 Educational License

This software is provided free for educational and non-profit use. For commercial licensing inquiries, please contact paracelsus12@gmail.com.
