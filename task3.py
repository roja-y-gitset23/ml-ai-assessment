"""Task 3: Tokens, cost, temperature and hallucination (Gemini API)."""
import os
import tiktoken
from dotenv import load_dotenv

load_dotenv()

# ---- EDIT THESE: use the prices given by your trainer (USD per 1 million tokens) ----
INPUT_PRICE_PER_M = float(os.getenv("INPUT_PRICE_PER_M", "0.15"))
OUTPUT_PRICE_PER_M = float(os.getenv("OUTPUT_PRICE_PER_M", "0.60"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# ---------- 1. TOKENS ----------
print("=== 1. TOKEN COUNT ===")
enc = tiktoken.get_encoding("cl100k_base")
texts = {
    "Short English sentence": "Please reset my password.",
    "Long English paragraph": "Our company provides support for billing, technical and account problems. "
                              "Customers can raise a ticket and the team replies within one business day.",
    "Python code": "def add(a, b):\n    return a + b\nprint(add(2, 3))",
    "Tamil text": "எனது கடவுச்சொல்லை மீட்டமைக்க உதவுங்கள்",
}
print("| Text | Words | Tokens | Words/token |\n|---|---|---|---|")
for name, t in texts.items():
    w, k = len(t.split()), len(enc.encode(t))
    print(f"| {name} | {w} | {k} | {w / k:.2f} |")

# ---------- 2. COST ----------
print("\n=== 2. MONTHLY COST ===")
chats_per_day, in_tok, out_tok, days = 300, 1200, 300, 30
monthly_in = chats_per_day * in_tok * days     # 10,800,000
monthly_out = chats_per_day * out_tok * days   # 2,700,000
cost_in = monthly_in / 1e6 * INPUT_PRICE_PER_M
cost_out = monthly_out / 1e6 * OUTPUT_PRICE_PER_M
print("| Item | Tokens/month | Price per 1M | Cost (USD) |\n|---|---|---|---|")
print(f"| Input | {monthly_in:,} | {INPUT_PRICE_PER_M} | {cost_in:.2f} |")
print(f"| Output | {monthly_out:,} | {OUTPUT_PRICE_PER_M} | {cost_out:.2f} |")
print(f"| **Total** | | | **{cost_in + cost_out:.2f}** |")

# ---------- 3 and 4 need the API ----------
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("\nSet GEMINI_API_KEY in .env to run parts 3 and 4.")
    raise SystemExit

from google import genai
from google.genai import types
client = genai.Client(api_key=api_key)

def ask(prompt, temperature=0.0, system=None):
    cfg = types.GenerateContentConfig(temperature=temperature, system_instruction=system,
                                      max_output_tokens=300)
    return client.models.generate_content(model=MODEL, contents=prompt, config=cfg).text.strip()

# ---------- 3. TEMPERATURE ----------
print("\n=== 3. TEMPERATURE ===")
prompt = "Write a one-sentence slogan for a company that sells coffee."
for temp in (0.0, 1.0):
    answers = [ask(prompt, temp) for _ in range(5)]
    print(f"\nTemperature {temp}: {len(set(answers))} different answers out of 5")
    for i, a in enumerate(answers, 1):
        print(f"  {i}. {a}")
print("\n| Temperature | Distinct answers (of 5) | Observation |\n|---|---|---|")
print("| 0.0 | see above | Almost identical, stable and repeatable |")
print("| 1.0 | see above | Different wording each time, more creative |")

# ---------- 4. HALLUCINATION ----------
print("\n=== 4. HALLUCINATION ===")
fake = "What were the main terms of the Zorvian Trade Accord signed in 2019 between Norway and Peru?"
plain = ask(fake, 0.7)
safe = ask(fake, 0.7, system="If you are not sure about a fact, say 'I don't know'. Do not guess.")
print("| Prompt style | Answer |\n|---|---|")
print(f"| Without 'say I don't know' | {plain[:250]!r} |")
print(f"| With 'say I don't know if unsure' | {safe[:250]!r} |")
print("\nObservation: without the instruction the model may invent details; with it, it should admit it does not know.")



