import argparse
import os
import sys

from web_search import web_search
from web_parser import parse_webpage
from summarizer import summarize
from evaluator import evaluate_answer
from guardrails import input_guardrail, output_guardrail
from logger import log_step

from config import (
    MAX_SEARCH_RESULTS,
    MAX_CONTENT_LENGTH,
    OUTPUT_DIR,
    LOG_DIR,
    MAX_RETRIES
)


# ---------- SETUP ----------
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


# ---------- CLI ----------
parser = argparse.ArgumentParser(
    description="Smart Research Assistant Agent"
)

parser.add_argument(
    "--query",
    type=str,
    required=True,
    help="Research question"
)

args = parser.parse_args()
question = args.query.strip()


# ---------- INPUT GUARD ----------
if not input_guardrail(question):
    print("❌ Input blocked by guardrails")
    log_step("BLOCKED INPUT")
    sys.exit()


log_step("START")
log_step(f"QUESTION: {question}")


# ---------- PIPELINE ----------
retry = 0
final_answer = None
sources = []


while retry < MAX_RETRIES:

    try:

        # SEARCH
        log_step("SEARCH: Started")
        results = web_search(question, MAX_SEARCH_RESULTS)

        if not results:
            raise Exception("No search results")


        # PARSE
        log_step("PARSE: Started")
        content = ""

        for r in results:

            url = r["url"]

            try:
                log_step(f"FETCH: {url}")

                text = parse_webpage(url)

                content += text[:MAX_CONTENT_LENGTH]
                sources.append(url)

                log_step(f"FETCH SUCCESS: {url}")

            except Exception as e:
                log_step(f"FETCH FAILED: {url} | {e}")


        if not content.strip():
            raise Exception("No usable content")


        # SUMMARIZE
        log_step("SUMMARIZE: Started")

        answer = summarize(content, question)


        # EVALUATE
        log_step("EVALUATE: Started")

        if not evaluate_answer(answer, question):
            raise Exception("Evaluation failed")


        # OUTPUT GUARD
        if not output_guardrail(answer):
            raise Exception("Output blocked")


        final_answer = answer
        break


    except Exception as e:

        retry += 1
        log_step(f"RETRY {retry}: {e}")


# ---------- FAILURE ----------
if not final_answer:
    print("❌ Failed after retries")
    log_step("STOP: Max retries")
    sys.exit()


# ---------- SAVE OUTPUT ----------
output_file = f"{OUTPUT_DIR}/answer.txt"


with open(output_file, "w", encoding="utf-8") as f:

    f.write("QUESTION:\n")
    f.write(question + "\n\n")

    f.write("ANSWER:\n")
    f.write(final_answer + "\n\n")

    f.write("SOURCES:\n")

    for s in sources:
        f.write("- " + s + "\n")


log_step("SUCCESS: Answer saved")


# ---------- PRINT ----------
print("\n✅ FINAL ANSWER\n")
print(final_answer)

print(f"\n📁 Saved to {output_file}")