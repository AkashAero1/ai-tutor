# AI Tutor Evaluation Environment

An OpenEnv-compliant RL environment where an LLM agent acts as an AI tutor.
The agent must identify student mistakes, explain concepts, and fix essays —
graded automatically with partial credit scoring.

---

## Problem

Students make mistakes in math, grammar, science, and writing every day.
Tutors must identify errors clearly, explain concepts simply, and
provide corrective feedback with explanations. This environment tests
whether an LLM can do all of that reliably.

---

## Environment Overview

| Property | Value |
|---|---|
| Tasks | 9 (3 easy, 3 medium, 3 hard) |
| Action space | Free-form text |
| Reward range | 0.0 – 1.0 |
| Max score | 9.0 (1.0 per task) |

---

## Tasks

### Easy (binary grading — 0 or 1)
- Identify an arithmetic mistake
- Identify a grammar error
- Identify a scientific misconception

### Medium (partial credit — keyword coverage ratio)
- Explain gravity to a 10-year-old
- Explain photosynthesis simply
- Explain simile vs metaphor with examples

### Hard (partial credit + length penalty)
- Fix a student essay with 6+ errors, explain each fix
- Rewrite a weak paragraph, explain all improvements
- Solve a multi-step word problem step-by-step

---

## API Endpoints

```
POST /reset   →  Start a new episode
POST /step    →  Submit an answer { "answer": "..." }
GET  /state   →  Get current state
GET  /health  →  Health check
GET  /tasks   →  List all tasks
```

---

## Reward Function

- **Easy**: Full credit (1.0) if the answer contains at least 2 of the expected keywords. Zero otherwise.
- **Medium**: Partial credit = matched_keywords / total_keywords. Must hit at least 3 keywords to score.
- **Hard**: Same as medium but penalised if answer is under 80 words (0.75×) or under 40 words (0.5×).

---

## Setup & Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Test it:
```bash
curl -X POST http://localhost:8000/reset
curl -X POST http://localhost:8000/step \
  -H "Content-Type: application/json" \
  -d '{"answer": "The student made an addition error. The correct answer is 43 not 33."}'
curl http://localhost:8000/state
```

---

## Run with Docker

```bash
docker build -t ai-tutor-env .
docker run -p 7860:7860 ai-tutor-env
```

---

## Run Inference

```bash
export API_BASE_URL="https://api-inference.huggingface.co/v1"
export MODEL_NAME="meta-llama/Llama-3.2-3B-Instruct"
export HF_TOKEN="your_hf_token"
export ENV_URL="http://localhost:7860"

python inference.py
```

---

## Action Space

Free-form text. The agent responds to the question in natural language.

```json
{ "answer": "The student made a carry error in addition. The correct answer is 43." }
```

## Observation Space

```json
{
  "task_id": "medium_1",
  "difficulty": "medium",
  "description": "Explain gravity to a 10-year-old student.",
  "question": "Explain gravity to a 10-year-old...",
  "step": 3,
  "total_tasks": 9,
  "cumulative_score": 2.75,
  "answered": false
}
```
