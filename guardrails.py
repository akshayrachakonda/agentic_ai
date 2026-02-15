def input_guardrail(question: str) -> bool:

    blocked = [
        "hack",
        "password",
        "private data",
        "steal",
        "illegal"
    ]

    for word in blocked:
        if word in question.lower():
            return False

    return True


def output_guardrail(answer: str) -> bool:

    bad_phrases = [
        "i think",
        "maybe",
        "probably",
        "not sure"
    ]

    for p in bad_phrases:
        if p in answer.lower():
            return False

    return True
