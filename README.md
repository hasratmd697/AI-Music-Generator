# 🎵 AI Music Generator

A full-stack AI-powered music generation application that creates custom songs from text descriptions, lyrics, or lyrical themes using state-of-the-art machine learning models.

![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vue.js)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)
![Modal](https://img.shields.io/badge/Modal-Serverless-FF6B6B)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-06B6D4?logo=tailwindcss)

## ✨ Features

### Three Generation Modes

- **Full Description**: Describe your song and let the AI generate music, lyrics, and cover art.
- **Custom Lyrics**: Provide your own lyrics with a music style prompt.
- **Described Lyrics**: Describe what the lyrics should be about, and the AI generates them.

### Modern UI/UX

- 🌙 Dark/Light mode with system preference detection
- 🎚️ Interactive audio player with waveform visualization
- ⚡ Playback speed control (0.5x - 2x)
- 🔔 Toast notifications for feedback
- 📱 Fully responsive design

### Audio Player

- WaveSurfer.js waveform visualization
- Play/Pause/Seek controls
- One-click download
- Variable playback speed

## 🛠️ Tech Stack

### Frontend

| Technology    | Purpose               |
| ------------- | --------------------- |
| Vue.js 3      | Reactive UI framework |
| Vite          | Fast build tool       |
| TailwindCSS   | Utility-first styling |
| Pinia         | State management      |
| WaveSurfer.js | Audio visualization   |
| Headless UI   | Accessible components |
| Lucide Icons  | Beautiful iconography |

### Backend

| Technology | Purpose                |
| ---------- | ---------------------- |
| Python     | Core language          |
| Modal      | Serverless GPU compute |
| FastAPI    | API endpoints          |
| MusicGen   | Audio generation model |

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- Modal account (for backend deployment)

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
modal deploy main.py
```

## 📁 Project Structure

```
AI-Music-Generator/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/       # Header, Footer, Notifications
│   │   │   ├── modes/        # Description, Lyrics, DescribedLyrics
│   │   │   ├── controls/     # Sliders, Toggles, Settings
│   │   │   ├── player/       # AudioPlayer, Waveform
│   │   │   └── results/      # GenerationResult
│   │   ├── stores/           # Pinia state management
│   │   ├── services/         # API configuration
│   │   └── composables/      # Reusable logic
│   └── ...
├── backend/
│   └── main.py               # Modal serverless functions
└── README.md
```

## 🎨 Screenshots

_Coming soon_

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
