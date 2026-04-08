from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import copy

from tasks import TASKS
from grader import grade

app = FastAPI(
    title="AI Tutor Evaluation Environment",
    description=(
        "An OpenEnv-compliant environment where an LLM agent acts as an AI tutor. "
        "The agent must identify student mistakes, explain concepts, and fix essays."
    ),
    version="1.0.0",
)


_state: dict = {}
_task_index: int = 0
_episode_history: list = []



class Action(BaseModel):
    answer: str  


class ResetResponse(BaseModel):
    task_id: str
    difficulty: str
    description: str
    question: str
    step: int
    total_tasks: int
    cumulative_score: float


class StepResponse(BaseModel):
    state: dict
    reward: float
    done: bool
    message: str



def _build_state(task: dict, step: int, cumulative_score: float) -> dict:
    return {
        "task_id": task["id"],
        "difficulty": task["difficulty"],
        "description": task["description"],
        "question": task["question"],
        "step": step,
        "total_tasks": len(TASKS),
        "cumulative_score": round(cumulative_score, 2),
        "answered": False,
    }



@app.get("/health")
def health():
    """Health check — must return 200 for HF Spaces validation."""
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    """Return all task IDs and descriptions."""
    return [
        {
            "id": t["id"],
            "difficulty": t["difficulty"],
            "description": t["description"],
        }
        for t in TASKS
    ]


@app.post("/reset")
def reset():
    """
    Start a new episode.
    Resets task index, history, and cumulative score.
    Returns the first task's state.
    """
    global _state, _task_index, _episode_history

    _task_index = 0
    _episode_history = []
    _state = _build_state(TASKS[_task_index], step=0, cumulative_score=0.0)

    return _state


@app.post("/step")
def step(action: Action):
    """
    Agent submits an answer.
    Grades it, updates state, advances to next task.
    Returns new state + reward + done flag.
    """
    global _state, _task_index, _episode_history

    if not _state:
        raise HTTPException(
            status_code=400,
            detail="Environment not initialised. Call POST /reset first."
        )

    if _state.get("answered"):
        raise HTTPException(
            status_code=400,
            detail="Current task already answered. Check /state for next task."
        )

    current_task = TASKS[_task_index]
    reward = grade(action.answer, current_task)

    _episode_history.append({
        "task_id": current_task["id"],
        "difficulty": current_task["difficulty"],
        "answer": action.answer,
        "reward": reward,
    })

    _state["answered"] = True
    cumulative = sum(h["reward"] for h in _episode_history)


    _task_index += 1
    done = _task_index >= len(TASKS)

    if not done:
        _state = _build_state(TASKS[_task_index], step=_task_index, cumulative_score=cumulative)
        message = f"Correct! Moving to task {_task_index + 1}/{len(TASKS)}."
    else:
        _state = {
            "task_id": "done",
            "difficulty": "none",
            "question": "Episode complete.",
            "step": _task_index,
            "total_tasks": len(TASKS),
            "cumulative_score": round(cumulative, 2),
            "answered": True,
        }
        message = f"Episode complete. Final score: {round(cumulative, 2)}/{len(TASKS)}"

    return StepResponse(
        state=_state,
        reward=reward,
        done=done,
        message=message,
    )


@app.get("/state")
def get_state():
    """Return current environment state."""
    if not _state:
        raise HTTPException(
            status_code=400,
            detail="Environment not initialised. Call POST /reset first."
        )
    return _state