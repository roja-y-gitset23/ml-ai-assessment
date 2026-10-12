# Task 3 - Tokens, Cost, Temperature and Hallucination  (all in one file)
# Run:  python task3.py      -> prints all results and creates results_tables.pdf
import os
import time

import tiktoken
from dotenv import load_dotenv
from google import genai
from google.genai import types
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# ------------------------------------------------------------------ settings from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
INPUT_PRICE = float(os.getenv("INPUT_PRICE_PER_M", "0.15"))     # USD per 1M input tokens
OUTPUT_PRICE = float(os.getenv("OUTPUT_PRICE_PER_M", "0.60"))   # USD per 1M output tokens

client = genai.Client(api_key=API_KEY)


def ask(prompt, temperature):
    """Call Gemini with retries. Returns the text, or an ERROR string."""
    last_error = ""
    for _ in range(4):
        try:
            resp = client.models.generate_content(
                model=MODEL, contents=prompt,
                config=types.GenerateContentConfig(temperature=temperature))
            time.sleep(2)
            return (resp.text or "").strip()
        except Exception as e:
            last_error = str(e)[:150]
            print("  retrying after error:", last_error)
            time.sleep(10)
    return "ERROR: " + last_error


# ------------------------------------------------------------------ POINT 1: tokens
print("=" * 60, "\nPOINT 1 - Token count (tiktoken cl100k_base)")
TEXTS = {
    "Short sentence": "Please reset my password.",
    "Paragraph": ("Large language models read text as tokens, which are small pieces of words. "
                  "The number of tokens decides how much a request costs and how much text "
                  "fits into the context window of the model."),
    "Python code": "def add(a, b):\n    return a + b\n\nprint(add(2, 3))",
    "Hindi text": "मुझे अपना पासवर्ड बदलने में मदद चाहिए, कृपया जल्दी सहायता करें।",
}
enc = tiktoken.get_encoding("cl100k_base")
table1 = []
print(f"{'Text':<16}{'Words':>7}{'Tokens':>8}{'Words/Token':>13}")
for name, text in TEXTS.items():
    words, tokens = len(text.split()), len(enc.encode(text))
    wpt = round(words / tokens, 2)
    table1.append([name, words, tokens, wpt])
    print(f"{name:<16}{words:>7}{tokens:>8}{wpt:>13}")

# ------------------------------------------------------------------ POINT 2: monthly cost
print("\n" + "=" * 60, "\nPOINT 2 - Monthly cost estimate")
CHATS_PER_DAY, IN_TOK, OUT_TOK, DAYS = 300, 1200, 300, 30
chats = CHATS_PER_DAY * DAYS
in_total, out_total = chats * IN_TOK, chats * OUT_TOK
in_cost = in_total / 1_000_000 * INPUT_PRICE
out_cost = out_total / 1_000_000 * OUTPUT_PRICE
total_cost = in_cost + out_cost
table2 = [
    ["Chats per month (300 x 30)", f"{chats:,}"],
    ["Input tokens per month", f"{in_total:,}"],
    ["Output tokens per month", f"{out_total:,}"],
    [f"Input cost (${INPUT_PRICE}/1M)", f"${in_cost:,.2f}"],
    [f"Output cost (${OUTPUT_PRICE}/1M)", f"${out_cost:,.2f}"],
    ["TOTAL monthly cost", f"${total_cost:,.2f}"],
]
for r in table2:
    print(f"{r[0]:<32}{r[1]:>16}")

# ------------------------------------------------------------------ POINT 3: temperature
print("\n=== 3. TEMPERATURE ===")
print("\n" + "=" * 60, "\nPOINT 3 - Temperature 0 vs 1.0 (5 runs each)")
PROMPT3 = "Write one short tagline for a coffee shop. Reply with the tagline only."
table3 = []
for temp in (0.0, 1.0):
    outs = []
    for run in range(1, 6):
        t = ask(PROMPT3, temp)
        outs.append(t)
        print(f"temp={temp} run {run}: {t}")
    table3.append([temp, f"{len(set(outs))} of 5", " | ".join(outs)])
for r in table3:
    print(f"Temperature {r[0]}: {r[1]} unique outputs")

# ------------------------------------------------------------------ POINT 4: hallucination

print("\n=== 4. HALLUCINATION ===")
print("\n" + "=" * 60, "\nPOINT 4 - Made-up fact with / without 'say I don't know'")
QUESTION = "Who won the 2019 Zorbian Prize in Quantum Gardening, and what was the winning paper about?"
GUARDED = QUESTION + " If you are not sure, say \"I don't know\"."
UNSURE = ["i don't know", "i do not know", "not aware", "no record", "cannot find", "can't find",
          "doesn't appear", "does not appear", "fictional", "not a real", "no information",
          "not familiar", "unable to find", "couldn't find", "no such", "does not exist"]


def verdict(text):
    t = text.lower().replace("\u2019", "'")
    return "Admitted not knowing" if any(k in t for k in UNSURE) else "Answered (hallucination)"


table4 = []
for label, prompt in (("Without guard", QUESTION), ("With 'say I don't know'", GUARDED)):
    ans = ask(prompt, 0.7)
    table4.append([label, verdict(ans), ans[:300]])
    print(f"\n[{label}] -> {verdict(ans)}\n{ans[:300]}")

# ------------------------------------------------------------------ PDF
styles = getSampleStyleSheet()
cell = styles["BodyText"].clone("cell"); cell.fontSize = 9; cell.leading = 11
head = styles["BodyText"].clone("head"); head.fontSize = 9; head.textColor = colors.white


def make_table(header, rows, widths):
    data = [[Paragraph(f"<b>{h}</b>", head) for h in header]]
    for r in rows:
        data.append([Paragraph(str(x).replace("&", "&amp;").replace("<", "&lt;"), cell) for x in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F4B7C")),
                           ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white])]))
    return t


story = [Paragraph("Task 3 - Tokens, Cost, Temperature and Hallucination", styles["Title"]),
         Paragraph(f"Model: {MODEL}", cell), Spacer(1, 0.3 * cm),
         Paragraph("1. Token count (tiktoken, cl100k_base)", styles["Heading3"]),
         make_table(["Text", "Words", "Tokens", "Words per token"], table1,
                    [5 * cm, 3 * cm, 3 * cm, 4 * cm]), Spacer(1, 0.4 * cm),
         Paragraph("2. Monthly cost (300 chats/day, 1200 input + 300 output tokens, 30 days)", styles["Heading3"]),
         make_table(["Item", "Value"], table2, [9 * cm, 6 * cm]), Spacer(1, 0.4 * cm),
         Paragraph("3. Temperature test (5 runs each)", styles["Heading3"]),
         Paragraph("Prompt: " + PROMPT3, cell),
         make_table(["Temperature", "Unique outputs", "The 5 outputs"], table3,
                    [2.5 * cm, 3 * cm, 11.5 * cm]), Spacer(1, 0.4 * cm),
         Paragraph("4. Hallucination test (made-up fact)", styles["Heading3"]),
         Paragraph("Question: " + QUESTION, cell),
         make_table(["Setting", "Result", "Model answer (first 300 chars)"], table4,
                    [3.5 * cm, 3.5 * cm, 10 * cm])]
SimpleDocTemplate("results_tables.pdf", pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                  topMargin=1.5 * cm, bottomMargin=1.5 * cm).build(story)
print("\nresults_tables.pdf created")