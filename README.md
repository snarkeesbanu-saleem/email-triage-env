# 📧 Email Triage Assistant

**Real-world Email Triage Environment** built for the **Scaler x Meta PyTorch OpenEnv Hackathon 2026 (Round 1)**

---

### 🎯 Project Overview

This project simulates a **smart AI Email Assistant** that helps companies handle incoming emails automatically. The agent receives emails and must:

- Classify the email correctly (Support, Sales, Complaint, etc.)
- Set appropriate priority (High / Medium / Low)
- Choose the right action (Reply, Archive, Escalate, Forward)
- Generate a professional reply when needed

### ✨ Key Features

- **3 Progressive Tasks** with increasing difficulty (Easy → Medium → Hard)
- **Deterministic Graders** that return scores between **0.0 - 1.0**
- **Meaningful Reward Shaping** with partial credit for good decisions
- Full compliance with **Meta OpenEnv** specification
- Clean Pydantic models for Action, Observation, and State
- Deployed as a Docker container on Hugging Face Spaces

### 🛠️ Tech Stack

- **Framework**: Meta OpenEnv + FastAPI
- **Language**: Python 3.12
- **Deployment**: Hugging Face Docker Space
- **Validation**: OpenEnv Validator

### 📍 Live Demo

**Hugging Face Space**:  
[https://narkeesbanu-email-triage-env.hf.space](https://narkeesbanu-email-triage-env.hf.space)

### 📋 Endpoints

| Endpoint       | Method | Description                      |
|----------------|--------|----------------------------------|
| `/`            | GET    | Health check                     |
| `/reset`       | POST   | Start new episode                |
| `/step`        | POST   | Submit agent action              |
| `/tasks`       | GET    | List tasks & action schema       |
| `/grader`      | POST   | Get average grader score         |
| `/baseline`    | GET    | Return baseline score            |

### 🏆 Hackathon Details

- **Event**: Scaler x Meta PyTorch OpenEnv Hackathon 2026
- **Round**: Round 1
- **Participant**: Narkees Banu (Solo Warrior)
- **Submission Date**: April 2026

---


Made with ❤️ for the Scaler x Meta Hackathon.

---

**Last Updated**: April 2026
