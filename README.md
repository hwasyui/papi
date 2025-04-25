# 🖼️ PAPI - Powerful Artistic Photo Innovator

**PAPI** is a powerful image preprocessing and editing application built with **Python**, **Tkinter**, and **OpenCV**. Designed for intuitive use and packed with a wide range of features, PAPI allows users to manipulate, enhance, and analyze images in-depth.

## ✨ Features

### 🔧 Basic Image Operations
- **Greyscale Conversion**: Convert images to greyscale via averaging or weighted RGB methods.
- **Negative Transformation**: Invert pixel values for negative image effects.
- **Color Manipulation**:
  - Convert areas to Red, Blue, or Yellow.
  - Adjust individual RGB intensities.
- **Flip Operations**:
  - Horizontal, Vertical, Diagonal.
- **Translation**: Move images by a custom offset.
- **Scaling**: Resize with or without maintaining aspect ratio.
- **Rotation**: Rotate in both directions by custom angles.
- **Cropping**: Crop rectangular or freeform regions.
- **Image Blending**: Merge two images with adjustable alpha blending.
- **Brightness & Contrast**:
  - Linear and nonlinear contrast.
  - Brightness via pixel intensity shift.
- **Color Filtering**:
  - Sepia, cyanotype, and custom filters.
- **Borders & Padding**: Add colorful frames or padding.
- **Image Overlay**: Stack images with custom position and transparency.

### 🧮 Mathematical Operations on Images
- **Pixel-wise**: Add, subtract, multiply, divide.
- **Bitwise**: AND, OR, XOR, NOT.

### ⚙️ Transforms & Filtering
- **Fourier Transform**: DFT and FFT support.
- **Spatial Filters**: Mean, Gaussian, Median.
- **Edge Detection**: Sobel, Canny, Laplacian.

### 🌈 Image Enhancement
- **Histogram Equalization**
- **Contrast Stretching**
- **Gamma Correction**

### 📦 Image Compression
- **Lossless**: Run-Length Encoding (RLE).
- **Lossy**: Discrete Cosine Transform (DCT).

### 🧩 Image Segmentation
- **Thresholding**: Global and adaptive.
- **K-Means Clustering**: Segment images into meaningful groups.

### ⚫ Binary Image Processing
- **Morphological Operations**: Dilation, Erosion, Opening, Closing.
- **Boundary Extraction & Skeletonization**

### 🛠️ Image Restoration
- **Noise Reduction**: Gaussian and Wiener filtering.
- **Inpainting**: Restore corrupted or missing regions.

### 🎯 Image Matching
- **Feature Detection**: SIFT or ORB algorithms.
- **Template Matching**: Locate objects in scenes.

---

## 🤝 Collaborators

This project was built through collaboration by the following contributors:

| Name | GitHub |
|------|--------|
| **Angelica Suti Whiharto** | [@hwasyui](https://github.com/hwasyui) |
| **Intan Kumala Pasya** | [@tannpsy](https://github.com/tannpsy) |
| **Rason Yudha Pati N** | [@RasonYudha4](https://github.com/RasonYudha4) |
| **Yoel Heardly Sirait** | [@heardlyyoel](https://github.com/heardlyyoel) |

---

## 🚀 Getting Started

### Requirements
- Python 3.8+
- OpenCV
- NumPy
- Tkinter

### Installation
```bash
git clone https://github.com/hwasyui/papi.git
cd papi
pip install -r requirements.txt
python environment.py

