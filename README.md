

# Interview.ai – AI Interview Evaluation Service

Interview.ai is a Python-based AI interview engine responsible for conducting interviews, evaluating candidate answers, generating follow-up questions, and producing structured interview reports.
It integrates Large Language Models (LLMs), Redis for session management, and Flask APIs for seamless communication with the frontend.

---

## Project Structure

```
AUTO_INTERVIEW/
│
├── service/
│   ├── ai_model.py
│   ├── llm_model.py
│   ├── interview_session.py
│
├── models/
│   ├── mistral-7b-instruct-v0.1.Q4_K_M.gguf
│
├── uploads/
│
├── migrations/
├── instance/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

---

## Prerequisites

* Python 3.10 or later
* Docker (for Redis)
* Redis (via Docker container)
* Virtual environment support (recommended)
* Local LLM runtime (GGUF-based model)

---

## Environment Configuration

Create a `.env` file in the root directory.

### `.env`

```env
FLASK_ENV=development
FLASK_APP=app.py
```

---

## Create Required Folders

Before running the application, ensure the following folders exist:

```bash
mkdir uploads
mkdir models
```

* `uploads/` is used to store uploaded resumes and temporary interview files.
* `models/` stores the local LLM model files.

---

## Download AI Model (Hugging Face)

This project uses a **local Mistral 7B Instruct model (GGUF format)**.

### Recommended Model

```
mistral-7b-instruct-v0.1.Q4_K_M.gguf
```

### Download Steps

1. Visit Hugging Face:

```
https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF
```

2. Download the file:

```
mistral-7b-instruct-v0.1.Q4_K_M.gguf
```

3. Place the model file inside:

```
interview_backend/models/
```

Final path:

```
interview_backend/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf
```

---

## Redis Setup (Docker)

Run Redis using Docker:

```bash
docker run -d \
  --name auto_interview_redis \
  -p 6379:6379 \
  redis:latest
```

Verify Redis is running:

```bash
docker ps
```

---

## Python Setup

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

The service will be available at:

```
http://127.0.0.1:5000
```

---

## Key Features

* AI-driven interview question flow
* Automatic answer evaluation and scoring
* Resume-aware follow-up questions
* Redis-backed session persistence
* Time-based interview control
* Structured final interview reports
* Scalable microservice architecture

---

## Development Notes

* AI evaluation logic is implemented in `service/ai_model.py`
* Interview session lifecycle is handled in `service/interview_session.py`
* LLM loading and prompt handling is managed in `service/llm_model.py`
* Designed to integrate with an external Node.js backend

---

## License

This project is intended for educational and professional use.
All rights reserved.

---

## Team

**SuPrazo Technologies**
Coded by **Suhen M. G** and **Sanjana M. Patil**

---

