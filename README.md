# 📧 Email Triage Assistant

**Real-world Email Triage Environment** built for the **Scaler x Meta PyTorch OpenEnv Hackathon 2026 (Round 1)**

---

### 🎯 Project Overview

This project is an **AI-powered Email Assistant** that processes incoming emails in a realistic setting. The agent must:

- Classify emails into categories (Support, Sales, Complaint, Spam, Internal)
- Assign correct priority (High, Medium, Low)
- Decide the appropriate action (Reply, Archive, Escalate, Forward)
- Generate polite and contextually accurate replies when needed

It features **3 progressive tasks** with increasing difficulty, designed to test agent capabilities in real-world customer support and inbox management scenarios.

### ✨ Key Features

- 3 tasks with clear difficulty progression (Easy → Medium → Hard)
- Deterministic graders that return scores between **0.0 – 1.0**
- Meaningful reward shaping with partial progress signals
- Full compliance with **Meta OpenEnv** framework
- Clean, typed Pydantic models for Action, Observation, and State
- Containerized deployment using Docker on Hugging Face Spaces

### 🛠️ Tech Stack

- **Core Framework**: Meta OpenEnv
- **Web Framework**: FastAPI
- **Language**: Python 3.12
- **Deployment**: Hugging Face Docker Space
- **Validation**: OpenEnv Validator

### 📍 Live Demo

**Hugging Face Space**:  
[https://narkeesbanu-email-triage-env.hf.space](https://narkeesbanu-email-triage-env.hf.space)

### 📋 Available Endpoints

| Method | Endpoint      | Description                          |
|--------|---------------|--------------------------------------|
| GET    | `/`           | Health check                         |
| POST   | `/reset`      | Start a new episode                  |
| POST   | `/step`       | Submit agent action                  |
| GET    | `/tasks`      | List tasks and action schema         |
| POST   | `/grader`     | Get average grader score             |
| GET    | `/baseline`   | Return baseline score                |

### 🏆 Hackathon Information

- **Event**: Scaler x Meta PyTorch OpenEnv Hackathon 2026
- **Round**: Round 1
- **Participant**: Narkees Banu (Solo Warrior)
- **Submission Date**: April 2026

---

Made with ❤️ for the Scaler x Meta Hackathon.

**Last Updated**: April 2026
