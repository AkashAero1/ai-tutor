import os
import json
import requests
from openai import OpenAI


ENV_URL      = os.environ.get("ENV_URL",      "http://localhost:8000")
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME   = os.environ.get("MODEL_NAME",   "gpt-4o-mini")
HF_TOKEN     = os.environ.get("HF_TOKEN",     "dummy")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN if HF_TOKEN else "dummy")

SYSTEM_PROMPT = """You are an expert AI tutor helping students learn.

You will be given a task that is one of:
1. Identifying a student's mistake — clearly name the error and explain why it's wrong.
2. Explaining a concept simply — use plain language with a real-life example.
3. Fixing a student essay — correct every error and explain each fix.

Always be specific, educational, and clear. Use keywords relevant to the subject."""


def run():
    step_num = 0
    total_reward = 0.0

    try:
        try:
            reset_resp = requests.post(f"{ENV_URL}/reset", timeout=30)
            state = reset_resp.json()
        except Exception as e:
            print(f"[END] total_steps=0 total_reward=0.0 max_possible=0 error=reset_failed:{e}")
            return

        print(f"[START] task_id={state.get('task_id','unknown')} total_tasks={state.get('total_tasks', 0)}")

        while True:
            question   = state.get("question",   "")
            difficulty = state.get("difficulty", "unknown")
            task_id    = state.get("task_id",    "unknown")
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    max_tokens=512,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user",   "content": question},
                    ],
                )
                answer = response.choices[0].message.content.strip()
            except Exception as e:
                answer = f"fallback answer due to llm error: {str(e)[:100]}"

            try:
                step_resp = requests.post(
                    f"{ENV_URL}/step",
                    json={"answer": answer},
                    timeout=30,
                )
                result = step_resp.json()
                reward = float(result.get("reward", 0.0))
                done   = bool(result.get("done",   False))
                state  = result.get("state", state)
            except Exception as e:
                print(f"[STEP] step={step_num} task_id={task_id} difficulty={difficulty} reward=0.0 total_reward={round(total_reward,2)} answer_preview=\"step_error\"")
                break

            total_reward += reward

            print(
                f"[STEP] step={step_num} "
                f"task_id={task_id} "
                f"difficulty={difficulty} "
                f"reward={reward} "
                f"total_reward={round(total_reward, 2)} "
                f"answer_preview={json.dumps(answer[:80])}"
            )

            step_num += 1

            if done:
                break

    except Exception as e:
        print(f"[END] total_steps={step_num} total_reward={round(total_reward,2)} max_possible={step_num} error={str(e)[:100]}")
        return

    print(
        f"[END] total_steps={step_num} "
        f"total_reward={round(total_reward, 2)} "
        f"max_possible={step_num} "
        f"final_state={json.dumps(state)}"
    )


if __name__ == "__main__":
    run()