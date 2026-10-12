# Runner file: tests the 3 queries, prints results, writes comparison_table.pdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from faq_data import FAQS, TEST_QUERIES
from search_engine import keyword_search, semantic_search

ids = [f[0] for f in FAQS]
questions = [f[2] for f in FAQS]

rows, wins = [], []
for query, expected, why in TEST_QUERIES:
    kw = keyword_search(query)
    sem = semantic_search(query, top_k=3)

    kw_text = "No match found" if not kw else "<br/>".join(
        f"{n}. [{ids[i]}] {questions[i]} (matched words: {s})" for n, (i, s) in enumerate(kw, 1))
    sem_text = "<br/>".join(
        f"{n}. [{ids[i]}] {questions[i]} (cosine {s:.2f})" for n, (i, s) in enumerate(sem, 1))
    rows.append((query, kw_text, sem_text))

    kw_correct = bool(kw) and ids[kw[0][0]] == expected
    sem_correct = ids[sem[0][0]] == expected
    if sem_correct and not kw_correct:
        wins.append((query, expected, why))

    print("=" * 70)
    print("QUERY:", query, f"(expected {expected})")
    print("  Keyword :", "No match" if not kw else [(ids[i], s) for i, s in kw])
    print("  Semantic:", [(ids[i], round(s, 2)) for i, s in sem])

print("\n" + "=" * 70)
print("SEMANTIC SEARCH WINS ON", len(wins), "QUERIES")
for q, exp, why in wins:
    print(f"- '{q}' -> {exp}: {why}")

# ------------------------------------------------------------- PDF
styles = getSampleStyleSheet()
cell = styles["BodyText"]; cell.fontSize = 9; cell.leading = 12
head = styles["BodyText"].clone("head"); head.fontSize = 10; head.textColor = colors.white

doc = SimpleDocTemplate("comparison_table.pdf", pagesize=landscape(A4),
                        leftMargin=1.5 * cm, rightMargin=1.5 * cm, topMargin=1.5 * cm, bottomMargin=1.5 * cm)
story = [Paragraph("Task 2 - Embeddings and Semantic Search: Comparison Table", styles["Title"]),
         Paragraph("Model: sentence-transformers all-MiniLM-L6-v2 | 12 FAQ questions (HR, IT, Payroll) | "
                   "cosine_similarity implemented with numpy", styles["BodyText"]),
         Spacer(1, 0.4 * cm)]

data = [[Paragraph("<b>Query</b>", head), Paragraph("<b>Keyword result</b>", head),
         Paragraph("<b>Semantic result (top 3)</b>", head)]]
for q, k, s in rows:
    data.append([Paragraph(q, cell), Paragraph(k, cell), Paragraph(s, cell)])
t = Table(data, colWidths=[4 * cm, 10.5 * cm, 12 * cm], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F4B7C")),
                       ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                       ("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white])]))
story += [t, Spacer(1, 0.6 * cm),
          Paragraph("Queries where semantic search wins", styles["Heading2"])]
if wins:
    for q, exp, why in wins:
        story.append(Paragraph(f"<b>'{q}'</b> (correct FAQ: {exp}): {why}", styles["BodyText"]))
        story.append(Spacer(1, 0.2 * cm))
else:
    story.append(Paragraph("Semantic search did not beat keyword search on these queries in this run.",
                           styles["BodyText"]))
doc.build(story)
print("\ncomparison_table.pdf created")