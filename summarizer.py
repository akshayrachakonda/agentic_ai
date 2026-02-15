from gemini_llm import call_llm
from research_prompt import RESEARCH_PROMPT


def summarize(content: str, question: str) -> str:
    prompt = RESEARCH_PROMPT.format(
        content=content,
        question=question
    )

    return call_llm(prompt, temperature=0)
