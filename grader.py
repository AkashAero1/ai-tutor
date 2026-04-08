
def grade(answer: str, task: dict) -> float:
    difficulty = task["difficulty"]
    keywords = task["expected_keywords"]
    min_keywords = task.get("min_keywords", 2)

    if difficulty == "easy":
        return _grade_easy(answer, keywords, min_keywords)
    elif difficulty == "medium":
        return _grade_medium(answer, keywords, min_keywords)
    elif difficulty == "hard":
        return _grade_hard(answer, keywords, min_keywords)
    return 0.0


def _grade_easy(answer: str, keywords: list, min_keywords: int) -> float:
    """
    Easy grader:
    - Full credit (1.0) if agent hits at least `min_keywords` keywords
    - Zero otherwise
    """
    matched = _count_matches(answer, keywords)
    return 1.0 if matched >= min_keywords else 0.0


def _grade_medium(answer: str, keywords: list, min_keywords: int) -> float:
    """
    Medium grader:
    - Partial credit based on ratio of matched keywords
    - Minimum bar: must hit at least `min_keywords` to score above 0
    - Score = matched / total keywords (capped at 1.0)
    """
    matched = _count_matches(answer, keywords)

    if matched < min_keywords:
        return 0.0

    score = matched / len(keywords)
    return round(min(score, 1.0), 2)


def _grade_hard(answer: str, keywords: list, min_keywords: int) -> float:
    """
    Hard grader:
    - Partial credit like medium
    - Extra penalty if answer is too short (shallow response)
    - Bonus for longer, more thorough answers
    """
    matched = _count_matches(answer, keywords)

    if matched < min_keywords:
        return 0.0

    base_score = matched / len(keywords)


    word_count = len(answer.split())
    if word_count < 40:
        base_score *= 0.5
    elif word_count < 80:
        base_score *= 0.75

    return round(min(base_score, 1.0), 2)


def _count_matches(answer: str, keywords: list) -> int:
    answer_lower = answer.lower()
    return sum(1 for kw in keywords if kw.lower() in answer_lower)
