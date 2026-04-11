import os
import json
import requests
from openai import OpenAI

SYSTEM_PROMPT = """You are an expert AI tutor helping students learn.
You will be given a task that is one of:
1. Identifying a student's mistake — clearly name the error and explain why it's wrong.
2. Explaining a concept simply — use plain language with a real-life example.
3. Fixing a student essay — correct every error and explain each fix.
Always be specific, educational, and clear. Use keywords relevant to the subject."""

def run():
    step_num = 0
    total_reward = 0.0
    state = {}

    try:
        ENV_URL      = os.environ.get("ENV_URL", "http://localhost:8000")
        API_BASE_URL = os.environ["API_BASE_URL"]
        API_KEY      = os.environ["API_KEY"]
        MODEL_NAME   = os.environ.get("MODEL_NAME", "gpt-4o-mini")

        client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

        try:
            state = requests.post(f"{ENV_URL}/reset", timeout=30).json()
        except Exception:
            print("[START] task_id=unknown total_tasks=0", flush=True)
            print("[END] total_steps=0 total_reward=0.0 max_possible=0 error=reset_failed", flush=True)
            return

        print(f"[START] task_id={state.get('task_id','unknown')} total_tasks={state.get('total_tasks',0)}", flush=True)

        while True:
            question   = state.get("question",   "")
            difficulty = state.get("difficulty", "unknown")
            task_id    = state.get("task_id",    "unknown")

            response = client.chat.completions.create(
                model=MODEL_NAME,
                max_tokens=512,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": question},
                ],
            )
            answer = response.choices[0].message.content.strip()

            try:
                result = requests.post(
                    f"{ENV_URL}/step",
                    json={"answer": answer},
                    timeout=30,
                ).json()
                reward = float(result.get("reward", 0.0))
                done   = bool(result.get("done",   False))
                state  = result.get("state", state)
            except Exception:
                reward = 0.0
                done   = True

            total_reward += reward
            print(
                f"[STEP] step={step_num} "
                f"task_id={task_id} "
                f"difficulty={difficulty} "
                f"reward={reward} "
                f"total_reward={round(total_reward, 2)} "
                f"answer_preview={json.dumps(answer[:80])}",
                flush=True
            )
            step_num += 1

            if done:
                break

    except Exception as e:
        print(f"[END] total_steps={step_num} total_reward={round(total_reward,2)} max_possible={step_num} error={str(e)[:200]}", flush=True)
        return

    print(
        f"[END] total_steps={step_num} "
        f"total_reward={round(total_reward, 2)} "
        f"max_possible={step_num} "
        f"final_state={json.dumps(state)}",
        flush=True
    )

if __name__ == "__main__":
    run()