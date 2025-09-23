# ThermoBreastAI: Hybrid AI for Breast Thermography Classification

[!\[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[!\[Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[!\[DOI](https://zenodo.org/badge/1062213182.svg)](https://doi.org/10.5281/zenodo.17180534)

> \\\*\\\*A Python library for computer-aided diagnosis of breast cancer using infrared thermography. Implements a hybrid AI approach combining transfer learning (CNNs) with classical ML classifiers.\\\*\\\*

`ThermoBreastAI` is a research software library designed for the scientific community working in medical imaging and AI-assisted diagnostics. It provides a modular, extensible framework to extract discriminative features from breast thermograms using pre-trained deep learning models (MobileNetV2, VGG19, ResNet) and classify them using classical machine learning algorithms (Random Forest, KNN, Naive Bayes).

Developed as part of the master's thesis *"Um Sistema Híbrido de Inteligência Artificial para Apoio ao Diagnóstico por Termografia de Mama em Dispositivos Móveis"* (Rian Rabelo de Azevedo, UPE, 2025), this library enables reproducible research in thermal breast cancer screening, particularly valuable in low-resource settings.

---

## Installation

```bash
pip install git+https://github.com/riansco14/ThermoBreastAI.git
```

## Quick Start

```python
from thermobreastai import HybridClassifier

# Initialize model
model = HybridClassifier(cnn\\\_model='ResNet', classifier='RandomForest')

# Paths to your thermographic images (JPEG/PNG)
image\\\_paths = \\\["path/to/image1.jpg", "path/to/image2.jpg"]
labels = \\\[1, 0]  # 1 = malignant, 0 = healthy

# Train the model
model.fit(image\\\_paths, labels)

# Predict on new images
test\\\_paths = \\\["path/to/new\\\_image.jpg"]
predictions = model.predict(test\\\_paths)
print(f"Prediction: {'Malignant' if predictions\\\[0] == 1 else 'Healthy'}")

# Evaluate performance (if you have ground truth)
# metrics = model.score(test\\\_paths, test\\\_labels)
# print(f"Accuracy: {metrics\\\['accuracy']:.3f}, Sensitivity: {metrics\\\['sensitivity']:.3f}")
```

## Features

* **Preprocessing:** Automatic metadata stripping and image resizing.
* **Feature Extraction:** Uses frozen pre-trained CNNs (ImageNet weights) for robust feature extraction.
* **Classification:** Supports Random Forest, KNN, and Naive Bayes with automated hyperparameter tuning (GridSearchCV).
* **Evaluation:** Computes accuracy, sensitivity, specificity, and confusion matrix.
* **Extensibility:** Easy to plug in new CNN architectures or classifiers.

## Included Sample Data

To help you get started, we include a small set of sample images in `data/sample\\\_images/`:

* **Format:** JPEG, 224x224 pixels
* **Quantity:** 5 images (for demonstration only)
* **License:** CC0 1.0 Universal (Public Domain)

⚠️ **Important:** These images are not sufficient for training. They are provided only to demonstrate software functionality. For real results, use your own dataset (e.g., from HC/UFPE).

## Running Tests

Ensure the core pipeline works:

```bash
pip install pytest
python -m pytest tests/ -v
```

## Citation

If you use ThermoBreastAI in your research, please cite the software and the original thesis:

```bibtex
@article{azevedo2025thermobreastai,
  author = {Rian Rabelo de Azevedo and 
            Adrielly Sayonara de Oliveira Silva and 
            José Barbosa de Araújo Neto and 
            Camila Tiodista de Lima and 
            Flávio Secco Fonseca and 
            Ana Clara Gomes da Silva and 
            Clarisse Lima and 
            Maíra Araújo de Santana and 
            Juliana Carneiro Gomes and 
            Giselle Machado Magalhães Moreno and 
            Wellington Pinheiro dos Santos},
  title = {{ThermoBreastAI}: A Hybrid AI Library for Breast Thermography Classification},
  journal = {Journal of Open Source Software},
  year = {2025},
  doi = {10.5281/zenodo.17180534},
  url = {https://github.com/AdriellySayonara/testedeploycanceria}
}



```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

