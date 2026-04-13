# Project Setup Log: VisionAI

Date: April 2, 2026

## Overview
VisionAI is an AI-powered image intelligence platform with a Next.js frontend and a Flask backend. The setup involved configuring both environments and resolving dependency conflicts.

## Issues Faced & Solutions

### 1. Python Dependency Conflict (NumPy)
- **Issue**: The `requirements.txt` specified `numpy<2`. On the current environment (Python 3.14 on Windows), this caused a build error because older NumPy versions attempted to build from source and failed with a GCC version mismatch error (`NumPy requires GCC >= 8.4`).
- **Solution**: Removed the `<2` constraint from `requirements.txt`. Installing the latest NumPy version (2.4.0) resolved the build compatibility issues.

### 2. Missing Backend Dependencies
- **Issue**: Initially, `flask-cors` and `diffusers` were missing from the environment, causing the Flask backend (`app.py`) to crash on startup.
- **Solution**: Performed a full `pip install -r requirements.txt`. Manually verified critical libraries (`diffusers`, `ultralytics`) before restarting the server.

### 3. Log Encoding Issues (Windows)
- **Issue**: Redirecting command output to files (`> log.txt`) on Windows PowerShell resulted in UTF-16 encoding, which the file viewer tool couldn't read correctly.
- **Solution**: Used PowerShell's `Get-Content | Out-File -Encoding utf8` to convert logs to standard UTF-8 format for analysis.

### 4. Background Server Initialization
- **Issue**: The backend server takes time to "warm up" (loading heavy ML models like Stable Diffusion and YOLO).
- **Solution**: Monitored the server logs until the warmup process started and verified the health endpoint (`/api/health`) responded with a 200 OK.

## Current Project Status
- **Frontend**: Running on [http://localhost:3000](http://localhost:3000) (Next.js Dev Server).
- **Backend**: Running on [http://localhost:8000](http://localhost:8000) (Flask API).
- **Models**: Warming up text-to-image and sketch-to-image pipelines.

## How to Start the Project in Future
1. Open a terminal for the backend: `python app.py`
2. Open a terminal for the frontend: `cd frontend && npm run dev`

### 5. Invalid File Type Error
- **Issue:** WebP files were mistakenly rejected due to .webp being absent from ALLOWED_EXTENSIONS. 
- **Solution:** Appended 'webp' to ALLOWED_EXTENSIONS in config.py.

### 6. Backend Crash / Warmup Failure
- **Issue:** Background warmup scripts for Text-to-Image and Sketch-to-Image ML pipelines executed simultaneously in parallel threads, resulting in an Out of Memory (OOM) crash during loading.
- **Solution:** Modified pp.py to initialize models sequentially inside a single thread, mitigating excessive memory spikes.
