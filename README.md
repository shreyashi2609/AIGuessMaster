# 🎯 AI Guess Master

> An engaging, intelligent number guessing game that challenges your logic and intuition.

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📖 Overview

**AI Guess Master** is a modern, interactive web application where players attempt to guess a secret number between 1 and 100. Unlike traditional guessing games, this project features a sophisticated **AI Assistant** that provides smart, context-aware hints to help you narrow down the possibilities.

Built with a robust **Flask** backend and a responsive, aesthetically pleasing **HTML5/CSS3** frontend, this game demonstrates clean architecture, state management, and real-time interaction.

## ✨ Key Features

- **🧠 Intelligent AI Assistant**:
  - Provides strategic hints based on your previous guesses.
  - Suggests optimal ranges and binary search strategies.
  - Adapts feedback based on how close you are.

- **🎮 Engaging Gameplay**:
  - Real-time feedback (Too High / Too Low).
  - Visual tracking of your guess history.
  - "Hot/Cold" indicators to guide your next move.

- **🎨 Modern UI/UX**:
  - **Responsive Design**: Works seamlessly on desktop and mobile devices.
  - **Aesthetic Visuals**: Beautiful SVG background patterns and smooth animations.
  - **Celebration Effects**: Confetti animations when you win!
  - **Accessibility**: Designed with ARIA labels and focus management.

- **🛠 Technical Excellence**:
  - **RESTful API**: Clean separation between frontend and backend.
  - **Session Management**: Secure server-side state tracking.
  - **Modular Codebase**: Well-structured Python and JavaScript code.

## 🏗 Tech Stack

### Backend
- **Python 3**: Core logic and server.
- **Flask**: Lightweight WSGI web application framework.
- **Flask-CORS**: Handling Cross-Origin Resource Sharing.
- **Werkzeug**: WSGI utility library.

### Frontend
- **HTML5**: Semantic markup.
- **CSS3**: Custom styling, flexbox/grid layouts, and animations.
- **JavaScript (ES6+)**: Dynamic DOM manipulation and async API calls.

## 🚀 Getting Started

Follow these instructions to set up the project on your local machine.

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1.  **Clone the repository** (if applicable) or navigate to the project root.

2.  **Set up the Backend**:
    ```bash
    # Install dependencies
    pip install -r requirements.txt
    ```

### Running the Application

You need to run both the backend and frontend servers. Open two terminal windows.

#### Terminal 1: Backend Server
```bash
python backend/app.py
```
*The backend will start on `http://localhost:5000`*

#### Terminal 2: Frontend Server
```bash
python frontend/server.py
```
*The frontend will start on `http://localhost:3000`*

### 🕹 How to Play

1.  Open your browser and navigate to `http://localhost:3000`.
2.  Click **"Start New Game"** to begin.
3.  Enter a number between **1 and 100** in the input field.
4.  Toggle **"Get AI hint"** if you want assistance.
5.  Click **"Guess!"** or press Enter.
6.  Read the feedback and adjust your strategy!
7.  Keep guessing until you find the secret number and trigger the celebration! 🎉

## 📂 Project Structure

```
.
├── backend/                # Flask Backend
│   ├── app.py              # Main API routes and server config
│   ├── game_logic.py       # Core rules and validation
│   ├── ai_hints.py         # AI hint generation engine
│   └── test_backend.py     # Unit tests
├── frontend/               # Frontend Application
│   ├── server.py           # Simple server for static files
│   └── static/
│       ├── templates/
│       │   └── index.html  # Main UI structure
│       ├── script.js       # Client-side logic & API integration
│       └── style.css       # Styling and animations
├── requirements.txt        # Python dependencies
└── test_connection.py      # Utility to verify backend connectivity
```

## 🔧 Configuration

- **Secret Key**: The Flask app uses a session secret key. For production deployment, update `app.secret_key` in `backend/app.py`.
- **Ports**:
  - Backend: 5000
  - Frontend: 3000
  - If you change these, ensure to update the CORS configuration in `backend/app.py` and `API_BASE_URL` in `frontend/static/script.js`.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---
Made with ❤️ by Jules
