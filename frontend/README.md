<div align="center">

# 🏙️ Vision AI — Special Eye Care Platform 👁️‍🗨️

### _"Seeing the Future of Eye Care, One Scan at a Time"_ 🗽✨

[![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-3178C6?style=for-the-badge&logo=typescript)](https://typescriptlang.org)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI%20Powered-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev)
[![Vite](https://img.shields.io/badge/Vite-6.x-646CFF?style=for-the-badge&logo=vite)](https://vitejs.dev)
[![Status](https://img.shields.io/badge/Status-%E2%9C%85%20Completed-brightgreen?style=for-the-badge)]()
[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Visit%20Now-FF6B6B?style=for-the-badge)](https://vision-ai-murex-five.vercel.app)

### 🌐 [**➡️ LIVE DEMO: vision-ai-murex-five.vercel.app**](https://vision-ai-murex-five.vercel.app) 🗽

</div>

---

## 🗺️ What is Vision AI?

> **Vision AI** is a next-generation, AI-powered clinical screening platform that unifies all **10 ICMR Eye Care Priority Topics** into a single, beautifully interactive diagnostic dashboard. Powered by **Google Gemini AI**, it performs multi-modal retinal image analysis with precision rivaling specialist clinicians — right from your browser. 🧠👁️

Think of it as the **Times Square** of eye care diagnostics — everything in one dazzling, high-powered hub! 🏙️🌟

> 🔗 **Try it live right now →** **[https://vision-ai-murex-five.vercel.app](https://vision-ai-murex-five.vercel.app)** ✨

---

## 🌆 Features at a Glance

| 🔍 Feature | 💡 Description |
|---|---|
| 🤖 **AI-Powered Diagnosis** | Upload retinal scans and receive instant multi-modal analysis via Google Gemini |
| 🏥 **10 ICMR Clinical Topics** | Covers all priority eye conditions: Diabetic Retinopathy, Glaucoma, Cataracts & more |
| 📊 **Analytics Dashboard** | Rich visual analytics showing diagnostic trends, severity distributions |
| 🧬 **Clinical Visualizer** | Deep-dive into diagnostic reports with annotated visual breakdowns |
| 💬 **Feedback Portal** | Clinicians can review, validate and submit expert feedback on AI findings |
| 🖼️ **Sample Scan Library** | Pre-loaded curated scans for testing and demonstration |
| 🔄 **High-Fidelity Simulator** | Works offline — generates realistic clinical reports without an API key |
| ⚡ **Real-Time Processing** | Low-latency image upload with retry logic and graceful error handling |
| 🎨 **Stunning UI/UX** | Glassmorphism, smooth animations, dark-mode-first design |
| 📱 **Fully Responsive** | Optimized for desktop, tablet, and mobile |

---

## 🗽 ICMR Eye Care Topics Covered

Vision AI covers all **10 priority ophthalmic conditions** mandated by the Indian Council of Medical Research:

```
🔵 01 — Diabetic Retinopathy        🟣 06 — Age-Related Macular Degeneration
🟢 02 — Glaucoma                    🟡 07 — Corneal Diseases
🔴 03 — Cataracts                   🟠 08 — Squint & Amblyopia
🟤 04 — Retinopathy of Prematurity  ⚪ 09 — Uveitis
🟦 05 — Childhood Blindness         🟥 10 — Ocular Oncology
```

---

## 🏗️ Project Architecture

```
vision-AI/
├── 🖥️  server.ts              ← Express backend + Gemini AI integration
├── 🌐  index.html             ← App entry point
├── ⚙️  vite.config.ts         ← Vite bundler configuration
├── 📦  package.json           ← Dependencies & scripts
├── 📁  src/
│   ├── 🧩  App.tsx            ← Root React component
│   ├── 🎨  index.css          ← Global styles (glassmorphism, animations)
│   ├── 📄  types.ts           ← TypeScript type definitions
│   ├── 📁  components/
│   │   ├── 📊  AnalyticsDashboard.tsx   ← Rich analytics charts & KPIs
│   │   ├── 🔬  ClinicalVisualizer.tsx   ← AI report deep-dive viewer
│   │   ├── 💬  FeedbackPortal.tsx       ← Clinician feedback system
│   │   ├── 🧭  Navbar.tsx               ← Navigation bar
│   │   ├── 🦶  Footer.tsx               ← Footer component
│   │   ├── 🗂️   SampleScansList.tsx     ← Pre-loaded scan library
│   │   ├── 🤖  AgentCard.tsx            ← AI agent info cards
│   │   └── 🏥  TopicDiagnosticGrid.tsx  ← ICMR topic grid interface
│   ├── 📁  sections/
│   │   ├── 🦸  HeroSection.tsx          ← Landing hero with animation
│   │   ├── ℹ️   AboutSection.tsx        ← About the platform
│   │   ├── ⭐  FeaturesSection.tsx      ← Feature highlights
│   │   ├── 🔧  TechnologySection.tsx    ← Tech stack showcase
│   │   ├── 🔄  WorkflowSection.tsx      ← How it works
│   │   ├── 🤖  AgentsSection.tsx        ← AI agents overview
│   │   └── 📞  ContactSection.tsx       ← Contact & links
│   └── 📁  data/                        ← Static clinical data
└── 📁  data/
    ├── 📋  diagnostics.json   ← Stored diagnostic records
    └── 📋  feedback.json      ← Clinician feedback records
```

---

## ⚡ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| ⚛️ **Frontend** | React 19 + TypeScript |
| ⚡ **Bundler** | Vite 6 |
| 🎨 **Styling** | TailwindCSS 4 + Custom Glassmorphism CSS |
| 🧠 **AI Engine** | Google Gemini API (`@google/genai`) |
| 🖥️ **Backend** | Node.js + Express 4 |
| 🎭 **Animations** | Motion (Framer Motion successor) |
| 🔣 **Icons** | Lucide React |
| 📦 **Runtime** | tsx (TypeScript Execute) |

</div>

---

## 🚀 Getting Started

### 📋 Prerequisites

- 🟢 **Node.js** v18 or higher
- 📦 **npm** v9+
- 🔑 **Google Gemini API Key** *(optional — platform runs in simulation mode without it)*

### 🛠️ Installation

```bash
# 1️⃣  Clone the repository
git clone https://github.com/challabhaskarrao/vision-AI.git
cd vision-AI

# 2️⃣  Install dependencies
npm install

# 3️⃣  (Optional) Set up your Gemini API Key
# Create a .env file in the root directory
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 4️⃣  Start the development server
npm run dev
```

> 🚀 **Or skip setup entirely — try the live demo at [https://vision-ai-murex-five.vercel.app](https://vision-ai-murex-five.vercel.app)**

> 🌐 Open your browser and navigate to **http://localhost:3000**

---

## 🎯 How It Works

```
🖼️ Upload Retinal Image
         ↓
🖥️ Express Server receives image
         ↓
🔑 API Key configured?
    ├── YES → 🤖 Gemini AI Multi-Modal Analysis
    └── NO  → 🔄 High-Fidelity Clinical Simulator
         ↓
📊 Diagnostic Report Generated
    ├── 🔬 Clinical Visualizer (deep-dive view)
    ├── 💾 Saved to Local Database
    └── 📈 Analytics Dashboard updated
         ↓
💬 Clinician Feedback & Validation
```

---

## 🗺️ NYC-Inspired Workflow (Borough by Borough! 🏙️)

```
🗽 MANHATTAN   → Upload & Analyze    (The Powerhouse — AI Diagnosis Core)
🌉 BROOKLYN    → Clinical Visualizer (The Creative Hub — Deep Report Review)
🌳 QUEENS      → Analytics Dashboard (The Diverse Thinker — Data Insights)
🏟️ BRONX       → Feedback Portal     (The Community Voice — Clinician Input)
⛴️ STATEN ISL. → Sample Scan Library (The Gateway — Pre-loaded Test Cases)
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API key for live AI analysis | ❌ Optional |

> 💡 **Tip**: Without an API key, Vision AI runs in **High-Fidelity Clinical Simulation Mode** — generating realistic diagnostic reports for demo and testing purposes!

---

## 🤝 Contributing

We welcome contributions from clinicians, researchers, and developers alike! 🙌

```bash
# Fork → Clone → Branch → Code → PR 🔁
git checkout -b feature/your-amazing-feature
git commit -m "✨ Add: your amazing feature"
git push origin feature/your-amazing-feature
```

---

## 🧑‍⚕️ Clinical Disclaimer

> ⚠️ **Vision AI is a research and educational tool.** It is NOT intended to replace professional medical diagnosis. Always consult a qualified ophthalmologist for clinical decisions.

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and share! 🎉

---

## 🙏 Acknowledgements

- 🇮🇳 **ICMR** — Indian Council of Medical Research for defining the 10 priority eye care topics
- 🤖 **Google Gemini** — For providing state-of-the-art multi-modal AI capabilities
- 🌐 **Open Source Community** — React, Vite, TypeScript, Lucide, Motion

---

<div align="center">

### 🏙️ Built with ❤️ for the future of eye care 👁️ — *NYC Style!* 🗽✨

**⭐ If you found this helpful, give it a star! It helps more clinicians find this tool! ⭐**

[![GitHub Stars](https://img.shields.io/github/stars/challabhaskarrao/vision-AI?style=social)](https://github.com/challabhaskarrao/vision-AI)

---

### 🌐 Live at: [vision-ai-murex-five.vercel.app](https://vision-ai-murex-five.vercel.app) 🚀

*🗺️ Manhattan → Brooklyn → Queens → Bronx → Staten Island — Vision AI covers it all, just like NYC covers everything! 🗽*

</div>
