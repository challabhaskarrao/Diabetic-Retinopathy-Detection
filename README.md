<div align="center">
  
  # 👁️ Diabetic Retinopathy AI Detection System
  
  **An enterprise-grade, hospital-ready Artificial Intelligence screening platform for early detection and grading of Diabetic Retinopathy.**
  
  [![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
  [![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C.svg?style=flat&logo=pytorch&logoColor=white)](https://pytorch.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
  [![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://reactjs.org/)
  [![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
  
</div>

---

## 🌟 Overview

The **Diabetic Retinopathy AI Detection System** is a state-of-the-art diagnostic support tool designed for ophthalmologists and healthcare clinics. Leveraging a deeply trained **EfficientNet-B3** Convolutional Neural Network (CNN), this system performs instantaneous analysis of retinal fundus images to detect, grade, and explain the severity of Diabetic Retinopathy (DR).

Boasting a stunning **White Frosted Glassmorphism UI**, the platform prioritizes clinical usability, trust, and explainability through advanced techniques like Grad-CAM visual heatmaps.

---

## ✨ Key Features

- 🏥 **Clinical-Grade UI/UX**: A pristine, modern, full-screen dashboard built with React and Tailwind CSS, featuring subtle micro-animations and frosted glass aesthetics tailored for medical environments.
- 🧠 **Deep Learning Inference**: Powered by PyTorch and EfficientNet-B3, providing 5-tier classification (No DR, Mild, Moderate, Severe, Proliferative).
- 🛡️ **Image Quality Assessment (IQA)**: Automatically rejects blurred, under-exposed, or poorly cropped scans before inference to prevent AI hallucinations.
- 🔍 **Grad-CAM Explainability**: Demystifies the "black box" by generating an overlaid heatmap highlighting the exact retinal regions (microaneurysms, hemorrhages, exudates) that influenced the AI's decision.
- 📊 **Probability Distributions**: Transparent confidence metrics mapped across all 5 diagnostic grades.
- 📋 **Automated Medical Reports**: Instant generation of PDF diagnostic reports containing patient metadata, AI findings, and actionable management plans based on clinical risk.

---

## 🏗️ System Architecture

This repository is structured into two completely decoupled microservices:

### 1. 🖥️ Backend (`/backend`)
A robust RESTful API pipeline serving the AI model.
- **Framework**: FastAPI (Python)
- **Model**: PyTorch (EfficientNet-B3)
- **Endpoints**: 
  - `/api/upload`: Secure image ingestion and session management.
  - `/api/image-quality`: Heuristic and AI-based image quality gating.
  - `/api/predict`: Core inference engine.
  - `/api/gradcam`: Generates visual explainability heatmaps.
  - `/api/generate-report`: Compiles PDF patient reports.

### 2. 🎨 Frontend (`/frontend`)
A highly responsive single-page application (SPA).
- **Framework**: React.js (Vite) + TypeScript
- **Styling**: Tailwind CSS + Custom Vanilla CSS for Glassmorphism.
- **State Management**: React Hooks (Strict Separation of Concerns).
- **Design Philosophy**: Zero-clutter, workflow-first layout prioritizing information hierarchy and instantaneous visual feedback.

---

## 🚀 Getting Started

### Prerequisites
- **Node.js** (v18+)
- **Python** (3.9+)
- **NVIDIA GPU** (Optional but highly recommended for fast inference)

### ⚙️ Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

### 🌐 Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Open your browser and navigate to `http://localhost:3000`.

---

## 🔬 Scientific Background

Diabetic retinopathy is a microvascular complication of diabetes and a leading cause of global blindness. Early screening is critical. Our EfficientNet-B3 architecture was chosen for its optimal balance between computational efficiency and feature-extraction accuracy, particularly in identifying subtle pathological lesions like:
- **Microaneurysms**
- **Dot and Blot Hemorrhages**
- **Hard Exudates**
- **Cotton Wool Spots**

---

## ⚖️ Disclaimer

**Medical Device Disclaimer**: This software is intended for **research and clinical decision-support purposes only**. It does not replace the professional judgment of a certified ophthalmologist. All AI-generated findings must be independently verified by medical professionals before any clinical intervention.

---

<div align="center">
  <i>Designed and engineered with ❤️ for the future of healthcare.</i>
</div>
