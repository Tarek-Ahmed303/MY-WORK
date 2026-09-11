# 🤟 American Sign Language (ASL) Image Classification

A Deep Learning and Computer Vision project for recognizing **American Sign Language (ASL) hand gestures from images** using different Convolutional Neural Network (CNN) architectures.

The project includes implementations and experiments with **Custom CNN, LeNet, and ResNet50**, along with sample images for testing the trained models.

---

## 📌 Project Overview

American Sign Language (ASL) is a visual language that uses hand gestures and movements for communication.

This project applies **Deep Learning and Computer Vision** techniques to automatically classify ASL hand gesture images into their corresponding signs.

Several CNN architectures are explored and compared to understand how different network designs perform on the ASL image classification task.

### Models Used

- 🧠 Custom CNN
- 🏗️ LeNet
- 🚀 ResNet50

---

## 📂 Project Structure

```text
ASL/
│
├── CNN/
│   └── Custom CNN model and related files
│
├── LENET/
│   └── LeNet model and related files
│
├── RESNET50/
│   └── ResNet50 model and related files
│
├── TEST_SAMPLES/
│   └── Sample ASL images used for testing
│
└── TEST_CODE_CV.ipynb
    └── Jupyter Notebook for testing and evaluating the models
```

---

## 🧠 Models

### 1. Custom CNN

A custom Convolutional Neural Network designed for ASL image classification.

The model uses fundamental CNN components such as:

- Convolutional layers
- Pooling layers
- Activation functions
- Fully connected layers
- Classification output layer

The custom CNN serves as a baseline model for the project.

---

### 2. LeNet

**LeNet** is a classic Convolutional Neural Network architecture and one of the early successful CNN models.

It is included in this project to provide a lightweight architecture for comparison with the custom CNN and the deeper ResNet50 model.

LeNet demonstrates how a relatively simple CNN can be applied to image classification tasks.

---

### 3. ResNet50

**ResNet50** is a deep Convolutional Neural Network architecture containing 50 layers.

It introduces **residual connections**, which help deep networks learn more effectively by allowing information to flow through shortcut connections.

ResNet50 is used in this project to evaluate the performance of a deeper and more advanced CNN architecture for ASL classification.

---

## 🔬 Project Workflow

The overall workflow of the project can be summarized as:

```text
             ASL Images
                 │
                 ▼
        Image Preprocessing
                 │
                 ▼
       Dataset Preparation
                 │
                 ▼
      ┌─────────────────────┐
      │                     │
      ▼                     ▼
    Training             Testing
      │                     │
      ▼                     ▼
 ┌───────────┐        Test Samples
 │ CNN       │             │
 │ LeNet     │             │
 │ ResNet50  │             │
 └───────────┘             │
      │                     │
      └──────────┬──────────┘
                 ▼
          Model Prediction
                 │
                 ▼
          ASL Classification
```

---

## 🖼️ Testing

The `TEST_SAMPLES` directory contains sample ASL images that can be used to evaluate the trained models.

The `TEST_CODE_CV.ipynb` notebook provides the testing workflow.

The testing process includes:

1. Loading a trained model
2. Loading an ASL image
3. Preprocessing the image
4. Passing the image through the model
5. Generating the predicted class
6. Evaluating the prediction

---

## 📊 Model Comparison

The project allows different CNN architectures to be compared based on their classification performance.

| Model | Architecture Type | Complexity | Main Purpose |
|---|---|---:|---|
| Custom CNN | Custom CNN | Medium | Baseline model |
| LeNet | Classic CNN | Low | Lightweight architecture |
| ResNet50 | Deep CNN | High | Deep/advanced architecture |

Possible evaluation metrics include:

- Accuracy
- Loss
- Validation Accuracy
- Validation Loss
- Confusion Matrix
- Prediction Results

---

## 🛠️ Technologies & Libraries

- **Python**
- **TensorFlow**
- **Keras**
- **NumPy**
- **OpenCV**
- **Matplotlib**
- **Jupyter Notebook**

### Concepts

- Deep Learning
- Computer Vision
- Image Classification
- Convolutional Neural Networks
- Transfer Learning
- Model Evaluation

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Install the Required Libraries

```bash
pip install tensorflow numpy opencv-python matplotlib jupyter
```

### 3. Open the Jupyter Notebook

```bash
jupyter notebook TEST_CODE_CV.ipynb
```

### 4. Test the Models

Place your test images inside:

```text
TEST_SAMPLES/
```

Then run the cells in `TEST_CODE_CV.ipynb` to load the trained models and generate predictions.

---

## 🎯 Project Objectives

The main objectives of this project are to:

- Build an ASL image classification system
- Apply Deep Learning to Computer Vision
- Implement and experiment with multiple CNN architectures
- Understand the differences between CNN architectures
- Compare lightweight and deep CNN models
- Test trained models on unseen ASL images
- Explore practical applications of AI for sign language recognition

---

## 🔮 Future Improvements

Possible future improvements include:

- 📷 Real-time ASL recognition using a webcam
- 🎥 Recognition of dynamic ASL gestures from video
- 📈 Hyperparameter optimization
- 🔄 Data augmentation
- 🧠 Improved model architectures
- ⚡ Model optimization for faster inference
- 📱 Deployment as a mobile or web application
- 🤖 Real-time hand detection combined with ASL classification
- 🌐 Building an interactive ASL recognition application

---

## 💡 Applications

An ASL recognition system can potentially be used in:

- Accessibility applications
- Educational tools
- Sign language learning systems
- Human-computer interaction
- Assistive technologies
- Real-time communication systems

---

## 👨‍💻 Skills Demonstrated

**Python • Deep Learning • Computer Vision • CNN • LeNet • ResNet50 • TensorFlow • Keras • OpenCV • NumPy • Image Classification • Model Evaluation • Jupyter Notebook**

---

## ⭐ Conclusion

This project demonstrates the use of different **Convolutional Neural Network architectures for American Sign Language image classification**.

By experimenting with a custom CNN, LeNet, and ResNet50, the project provides a practical comparison of different approaches to image-based sign language recognition.

---

## 📜 License

This project is intended for educational and research purposes.
