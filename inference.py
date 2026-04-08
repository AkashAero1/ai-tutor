import os
import json
import requests
import google.generativeai as genai
import dotenv

dotenv.load_dotenv()


ENV_URL = os.environ.get("ENV_URL", "http://localhost:8000")

API_BASE_URL = os.environ.get("API_BASE_URL", "https://generativelanguage.googleapis.com")
MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-2.5-flash")
HF_TOKEN = os.environ.get("HF_TOKEN")  


genai.configure(api_key=HF_TOKEN)

model = genai.GenerativeModel(MODEL_NAME)


SYSTEM_PROMPT = """You are an expert AI tutor helping students learn.

You will be given a task that is one of:
1. Identifying a student's mistake — clearly name the error and explain why it's wrong.
2. Explaining a concept simply — use plain language with a real-life example.
3. Fixing a student essay — correct every error and explain each fix.

Always be specific, educational, and clear. Use keywords relevant to the subject.

IMPORTANT:
Your answer will be evaluated based on keyword coverage and explanation quality.

Make sure to:
- Include relevant subject keywords naturally
- Give a clear explanation
- Be sufficiently detailed (at least 80+ words for complex tasks)
"""


def run():
    state = requests.post(f"{ENV_URL}/reset").json()
    print(f"[START] task_id={state['task_id']} total_tasks={state['total_tasks']}")

    step_num = 0
    total_reward = 0.0

    while True:
        question = state.get("question", "")
        difficulty = state.get("difficulty", "")
        task_id = state.get("task_id", "")

        full_prompt = f"{SYSTEM_PROMPT}\n\nStudent Question:\n{question}"

        response = model.generate_content(full_prompt)

        answer = response.text.strip()

        result = requests.post(
            f"{ENV_URL}/step",
            json={"answer": answer},
        ).json()

        reward = result["reward"]
        done = result["done"]
        total_reward += reward

        print(
            f"[STEP] step={step_num} "
            f"task_id={task_id} "
            f"difficulty={difficulty} "
            f"reward={reward} "
            f"total_reward={round(total_reward, 2)} "
            f"answer_preview={json.dumps(answer[:80])}"
        )

        state = result["state"]
        step_num += 1

        if done:
            break

    print(
        f"[END] total_steps={step_num} "
        f"total_reward={round(total_reward, 2)} "
        f"max_possible={step_num} "
        f"final_state={json.dumps(state)}"
    )


if __name__ == "__main__":
    run()