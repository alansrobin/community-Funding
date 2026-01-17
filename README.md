# Behavior-Aware and Ethical Automated Fund Collection System

**A human-centric, AI-driven platform for community welfare organizations.**

This repository contains the full source code for the "Behavior-Aware and Ethical Automated Fund Collection System", a solution designed to automate fund collection while preserving member dignity through behavioral analytics and ethical nudging.

## 📂 Project Structure

This project is divided into two main components:

*   **[Backend (`/backend`)](./backend/README.md)**: A FastAPI (Python) server that handles the database, authentication, predictive analytics, and automated functionality.
*   **[Frontend (`/frontend`)](./frontend/README.md)**: A React (Vite) application that provides the user interface for both members and administrators.

## 🚀 Quick Start Guide

To get the full system running, you need to start both the backend and the frontend.

### Prerequisites
*   Node.js (v16+)
*   Python (v3.8+)
*   MongoDB (Local running on port 27017 or Atlas URI)

### 1. Backend Setup
Navigate to the `backend` folder and follow the detailed instructions in [backend/README.md](./backend/README.md).

```bash
cd backend
python -m venv venv
# Activate venv (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
# Create .env file as per instructions
python init_db.py # Optional: Create demo data
uvicorn main:app --reload
```

### 2. Frontend Setup
Open a new terminal, navigate to the `frontend` folder, and follow the instructions in [frontend/README.md](./frontend/README.md).

```bash
cd frontend
npm install
npm run dev
```

## 🌟 Key Features

*   **Behavior-Aware Intelligence**: ML-driven analysis of payment patterns.
*   **Ethical Nudging**: Personalized, non-coercive reminders.
*   **Dual Interface**: Dedicated dashboards for Admins and Members.
*   **Automated Scheduler**: Daily checks for upcoming or overdue payments.
*   **Privacy First**: Secure authentication and data handling.

## 🔗 Documentation

For detailed documentation, please refer to the specific READMEs for each part of the stack:

*   📘 **[Backend Documentation](./backend/README.md)** (API, Database, Logic)
*   📙 **[Frontend Documentation](./frontend/README.md)** (UI, Components, Routing)
