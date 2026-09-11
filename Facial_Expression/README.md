# Facial Expression Recognition Models

The Facial Expression Recognition module was evaluated using three deep learning architectures:

- **YOLOv8n (Nano)**
- **YOLOv8m (Medium)**
- **ResNet50 (Transfer Learning + Fine-Tuning)**

---

## Model Comparison

| Model | Parameters | Model Size | Speed | Accuracy | GPU Memory |
|-------|-----------:|-----------:|-------|----------|------------|
| **YOLOv8n** | ~3.2M | ~6 MB | ⭐⭐⭐⭐⭐ Very Fast | ~82% mAP50 | Low |
| **YOLOv8m** | ~25.9M | ~50 MB | ⭐⭐⭐ Moderate | Higher mAP50 | Medium |
| **ResNet50** | ~25.6M | ~98 MB | ⭐⭐⭐ Moderate | **93% Validation Accuracy** | Medium |

---

# YOLOv8n (Nano)

## Characteristics
- Lightweight architecture
- Fast training and inference
- Low VRAM requirements
- Suitable for real-time applications and edge devices

## Advantages
- High inference speed
- Easy deployment
- Lower computational cost
- Suitable for laptops with limited GPU memory

## Limitations
- Lower feature extraction capacity
- May struggle with subtle facial expressions
- Generally achieves lower mAP than larger models

## Use Cases
- Real-Time Facial Expression Recognition
- Embedded Devices
- Low-Latency Applications

---

# YOLOv8m (Medium)

## Characteristics
- Larger backbone and neck architecture
- Higher representational capacity
- Better feature extraction

## Advantages
- Improved classification performance
- Better handling of difficult classes
- Higher mAP and recall
- More robust to lighting and pose variations

## Limitations
- Higher GPU memory consumption
- Slower training and inference
- Longer experimentation cycles

## Use Cases
- Research Projects
- High-Accuracy Applications
- Server Deployment
- Offline Analysis Systems

---

# ResNet50 (Transfer Learning + Fine-Tuning)

## Characteristics
- Pretrained on ImageNet
- Transfer learning with staged fine-tuning
- Deep residual architecture
- Optimized for image classification

## Advantages
- **93% validation classification accuracy**
- Excellent facial feature extraction
- Strong generalization
- Robust to pose and illumination changes

## Limitations
- Larger than YOLOv8n
- Slower than lightweight models
- Classification only (not object detection)

## Use Cases
- Smart Interview Systems
- Emotion Recognition
- Facial Expression Classification
- AI Behavioral Analysis

---

# Overall Comparison

| Metric | YOLOv8n | YOLOv8m | ResNet50 |
|--------|:-------:|:-------:|:--------:|
| Training Speed | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Inference Speed | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Memory Usage | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Accuracy | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Generalization | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Deployment Ease | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

# Experimental Results

## YOLOv8n
- ~82% mAP50
- Excellent real-time performance
- Low computational requirements

## YOLOv8m
- Higher mAP50 than YOLOv8n
- Better performance on difficult facial expressions
- Balanced accuracy and speed

## ResNet50
- **93% validation accuracy**
- Highest classification performance
- Stable convergence after transfer learning and fine-tuning

---

# Final Recommendation

| Model | Recommended For |
|-------|-----------------|
| **YOLOv8n** | Best for real-time applications and edge devices. |
| **YOLOv8m** | Best balance between detection accuracy and inference speed. |
| **ResNet50** | Best choice when maximum facial expression classification accuracy is required. |
