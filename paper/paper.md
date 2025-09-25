---
title: 'ThermoBreastAI: A Hybrid AI Library for Breast Thermography Classification'

tags:
  - medical imaging
  - breast cancer
  - infrared thermography
  - transfer learning
  - computer-aided diagnosis
  - deep learning
  - machine learning
  - python

authors:
  - name: Rian Rabelo de Azevedo
    orcid: 0009-0003-1816-9576
    affiliation: "1"
  - name: Adrielly Sayonara de Oliveira Silva
    orcid: 0009-0004-2220-8053
    affiliation: "2"
  - name: José Barbosa de Araújo Neto
    orcid: 0009-0007-4994-1695
    affiliation: "2"
  - name: Camila Tiodista de Lima
    orcid: 0009-0007-6013-7059
    affiliation: "2"
  - name: Flávio Secco Fonseca
    orcid: 0000-0003-4956-1135
    affiliation: "1"
  - name: Ana Clara Gomes da Silva
    orcid: 0000-0002-2823-5763
    affiliation: "2"
  - name: Clarisse Lima
    orcid: 0000-0003-1198-8627
    affiliation: "2"
  - name: Maíra Araújo de Santana
    orcid: 0000-0002-1796-7862
    affiliation: "2"
  - name: Juliana Carneiro Gomes
    orcid: 0000-0002-0785-0767
    affiliation: "2"
  - name: Giselle Machado Magalhães Moreno 
    orcid: 0000-0003-4076-3494
    affiliation: "2"
  - name: Wellington Pinheiro dos Santos
    orcid: 0000-0003-2558-6602
    affiliation: "1,2"

affiliations:
  - name: Graduate Program in Computer Engineering, University of Pernambuco, Brazil
    index: 1
  - name: Department of Biomedical Engineering, Federal University of Pernambuco, Brazil
    index: 2

date: 12 May 2025
bibliography: paper.bib
---

# Summary

**ThermoBreastAI** is a Python library for computer-aided diagnosis of breast cancer using infrared thermography. It implements a hybrid artificial intelligence approach that combines transfer learning — using frozen pre-trained convolutional neural networks (MobileNetV2, VGG19, ResNet) for feature extraction — with classical machine learning classifiers (Random Forest, KNN, Naive Bayes) for diagnostic prediction. Originally developed to support the research presented in [@azevedo2025], [@santana2018breast], [@macedo2021breast], this library provides a modular, extensible, and reproducible framework for researchers working on thermal breast cancer screening, particularly valuable in low-resource settings where access to mammography is limited.

While general-purpose medical imaging libraries exist, few offer specialized, validated pipelines for thermographic analysis. **ThermoBreastAI** fills this gap by providing exact implementations of a hybrid AI workflow optimized for small medical datasets, enabling reproducible research and clinical decision support.




# Statement of Need



Breast cancer is the most prevalent cancer among women worldwide [@sung2021]. Despite advances in screening, challenges such as accessibility, patient discomfort, and radiation exposure remain — especially in developing regions [@inca2022]. Infrared thermography offers a safe, non-invasive, low-cost alternative but suffers from subjective interpretation and lack of standardized analysis tools [@singh2020].



Existing AI tools for thermography are often:

- Research prototypes without reusable, documented code.

- Based solely on fine-tuning CNNs — prone to overfitting on small datasets [@rosliadar2019].

- Lacking modularity, making extension or comparison difficult.



**ThermoBreastAI** addresses these gaps by providing:

1. A **reusable, pip-installable Python library** — not a monolithic application.

2. A **hybrid AI architecture** optimized for small datasets: frozen CNNs + interpretable ML.

3. **Built-in evaluation metrics** aligned with clinical needs (e.g., sensitivity prioritized over accuracy).

4. **Full test coverage and documentation** — enabling reproducibility and community contribution.



# State of the Field



The application of artificial intelligence to breast thermography has gained traction in recent years, with studies demonstrating promising results using both classical machine learning and deep learning approaches.



Early work by [@vasconcelos2018] used statistical interval features and classical classifiers (e.g., SMO, Random Forest) on the HC/UFPE dataset, achieving 93.4% accuracy in binary classification. More recent studies have employed end-to-end CNNs: [@ekici2020] used a custom CNN architecture on UFF data to achieve 95.8% accuracy, while [@rosliadar2019] and [@chaves2020] applied fine-tuning to models like DenseNet and VGG19, reporting accuracies up to 100% and 77.5%, respectively.



However, these approaches often suffer from critical limitations:

- **Lack of reproducibility**: Code is rarely open-sourced or packaged for reuse.

- **Overfitting risk**: Fine-tuning on small medical datasets (<1000 images) can lead to inflated performance metrics.

- **Monolithic design**: Most implementations are scripts or notebooks, not modular libraries.



**ThermoBreastAI** advances the field by:

- Releasing a **fully open-source, tested, and documented library**.

- Introducing a **hybrid architecture\*\* that freezes CNN weights to prevent overfitting — a design choice validated by 100% sensitivity on clinical data.

- Providing **standardized evaluation metrics** (accuracy, sensitivity, specificity) and **automated hyperparameter tuning** via `GridSearchCV`.


# Software Description / Functionality



**ThermoBreastAI** offers a comprehensive suite of tools for preprocessing, feature extraction, classification, and evaluation of breast thermograms. It combines an intuitive Python interface with robust machine learning backends.


# Key Features



- **Preprocessing**: Automatic stripping of thermal metadata and resizing to 224x224 pixels for compatibility with pre-trained CNNs.

- **Feature Extraction**: Uses frozen CNN backbones (pre-trained on ImageNet) to extract robust, generalizable features — mitigating overfitting on small medical datasets.

- **Classification**: Supports Random Forest, KNN, and Naive Bayes with automated hyperparameter tuning via `GridSearchCV`.

- **Evaluation**: Computes standard clinical metrics: accuracy, sensitivity, specificity, and confusion matrix — prioritizing sensitivity for screening applications.

- **Extensibility**: Designed for easy integration of new CNN architectures or classifiers via subclassing.

- **Reproducibility**: Includes sample data and unit tests (`pytest`) to validate installation and core functionality.



# Example Usage



```python

from thermobreastai import HybridClassifier



# Initialize model

model = HybridClassifier(cnn_model='ResNet', classifier='RandomForest')



# Train on your dataset

image_paths = ["path/to/malignant.jpg", "path/to/healthy.jpg"]

labels = [1, 0]  #1 = malignant, 0 = healthy

model.fit(image_paths, labels)



# Predict and evaluate

test_paths = ["path/to/new_image.jpg"]

prediction = model.predict(test_paths)

print(f"Diagnosis: {'Malignant' if prediction\[0] == 1 else 'Healthy'}")



# Optional: Evaluate performance

# metrics = model.score(test_paths, test_labels)

# print(f"Sensitivity: {metrics['sensitivity']:.3f}")

```



# Installation \& Testing



```bash

pip install git+https://github.com/AdriellySayonara/testedeploycanceria



# Run tests

pip install pytest

python -m pytest tests -v

```



# Acknowledgements



This work was developed as part of the Master’s program at Universidade de Pernambuco, with support from Hospital das Clínicas da UFPE for dataset access. We thank the open-source communities of Python, TensorFlow, scikit-learn, and pytest. This software is released under the GNU General Public License v3.0 to ensure proper attribution to the original authors and to uphold the principles of ethical and reciprocal reuse in scientific software.



# References


