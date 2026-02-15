def evaluate_answer(answer: str, question: str) -> bool:

    if not answer:
        return False

    if len(answer.strip()) < 20:
        return False

    keywords = question.lower().split()

    matches = 0
    for k in keywords:
        if k in answer.lower():
            matches += 1

    return matches >= 1
