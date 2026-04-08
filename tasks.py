TASKS = [

    {
        "id": "easy_1",
        "difficulty": "easy",
        "description": "Identify the arithmetic mistake a student made.",
        "question": (
            "A student solved: 15 + 28 = 33. "
            "What mistake did the student make? Explain clearly."
        ),
        "expected_keywords": ["carry", "addition", "43", "wrong", "mistake", "incorrect"],
        "min_keywords": 2,
    },
    {
        "id": "easy_2",
        "difficulty": "easy",
        "description": "Identify a grammar mistake in a student's sentence.",
        "question": (
            "A student wrote: 'She don't like apples.' "
            "What is the grammatical mistake? Explain clearly."
        ),
        "expected_keywords": ["doesn't", "subject-verb", "agreement", "singular", "verb", "error"],
        "min_keywords": 2,
    },
    {
        "id": "easy_3",
        "difficulty": "easy",
        "description": "Identify a scientific misconception.",
        "question": (
            "A student says: 'The sun revolves around the earth.' "
            "What is the misconception here? Correct the student."
        ),
        "expected_keywords": ["earth", "revolves", "sun", "orbit", "center", "solar system", "wrong"],
        "min_keywords": 2,
    },


    {
        "id": "medium_1",
        "difficulty": "medium",
        "description": "Explain gravity to a 10-year-old student.",
        "question": (
            "Explain the concept of gravity to a 10-year-old student "
            "using simple language and a real-life example."
        ),
        "expected_keywords": ["pull", "earth", "falls", "force", "down", "example", "weight"],
        "min_keywords": 3,
    },
    {
        "id": "medium_2",
        "difficulty": "medium",
        "description": "Explain photosynthesis simply.",
        "question": (
            "A student asks: 'What is photosynthesis?' "
            "Explain it in simple terms suitable for a middle school student."
        ),
        "expected_keywords": ["sunlight", "water", "carbon dioxide", "oxygen", "food", "plant", "energy"],
        "min_keywords": 3,
    },
    {
        "id": "medium_3",
        "difficulty": "medium",
        "description": "Explain the difference between simile and metaphor.",
        "question": (
            "A student is confused about simile vs metaphor. "
            "Explain the difference with one example of each."
        ),
        "expected_keywords": ["like", "as", "comparison", "simile", "metaphor", "example", "directly"],
        "min_keywords": 3,
    },


    {
        "id": "hard_1",
        "difficulty": "hard",
        "description": "Correct a student essay and explain each fix.",
        "question": (
            "Fix this student essay and explain every correction:\n\n"
            "'Yesterday i go to school and learn many thing. "
            "The teacher were very kind and give we a test. "
            "I writed all the answer careful.'"
        ),
        "expected_keywords": [
            "went", "learned", "things", "was", "gave",
            "us", "wrote", "carefully", "capital", "tense"
        ],
        "min_keywords": 5,
    },
    {
        "id": "hard_2",
        "difficulty": "hard",
        "description": "Evaluate and improve a weak paragraph.",
        "question": (
            "A student wrote this paragraph about climate change:\n\n"
            "'Climate change is bad. It makes things hot. "
            "Animals die. We should do something about it.'\n\n"
            "Rewrite it to be more academic and detailed, "
            "then explain what you improved and why."
        ),
        "expected_keywords": [
            "temperature", "emissions", "habitat", "scientific",
            "evidence", "global warming", "improved", "specific",
            "vocabulary", "detail"
        ],
        "min_keywords": 4,
    },
    {
        "id": "hard_3",
        "difficulty": "hard",
        "description": "Solve a multi-step word problem and explain each step.",
        "question": (
            "Help a student understand this word problem step-by-step:\n\n"
            "'A train travels 60 km/h for 2 hours, then 80 km/h for 3 hours. "
            "What is the total distance traveled?'\n\n"
            "Solve it and explain each step clearly so the student understands."
        ),
        "expected_keywords": [
            "120", "240", "360", "distance", "speed", "time",
            "multiply", "step", "total", "formula"
        ],
        "min_keywords": 5,
    },
]