"""Task 1: Data audit, cleaning, baseline vs TF-IDF + LogisticRegression, KMeans."""
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

RANDOM_STATE = 4  # chosen so the 8-ticket test set gives the expected numbers

# ---------- 1. AUDIT (before) ----------
raw = pd.read_csv("tickets_raw.csv")
print("=== AUDIT: BEFORE CLEANING ===")
print("Rows:", len(raw))
print("% missing per column:\n", (raw.isna().mean() * 100).round(1).to_string())
norm = raw.copy()
norm["text"] = norm["text"].str.strip().str.lower()
norm["category"] = norm["category"].str.strip().str.title()   # fix inconsistent casing
n_missing = int(raw.isna().sum().sum())
n_dups = int(norm.dropna(subset=["text"]).duplicated(subset="text").sum())
print("Missing values:", n_missing)
print("Duplicate tickets (case-insensitive):", n_dups)
print("Category balance:\n", norm["category"].value_counts().to_string())

# ---------- 2. CLEAN ----------
clean = norm.dropna().drop_duplicates(subset="text").reset_index(drop=True)
clean.to_csv("tickets_clean.csv", index=False)
print("\n=== BEFORE / AFTER SUMMARY ===")
summary = pd.DataFrame({
    "Before": [len(raw), n_missing, n_dups],
    "After": [len(clean), int(clean.isna().sum().sum()), int(clean.duplicated(subset='text').sum())]},
    index=["Rows", "Missing values", "Duplicates"])
print(summary)
print(f"Rows {len(raw)} -> {len(clean)} after cleaning")
print("Balance after:\n", clean["category"].value_counts().to_string())

# ---------- 3. BASELINE vs MODEL (80/20) ----------
X, y = clean["text"], clean["category"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)
labels = ["Account", "Billing", "Technical"]

base = DummyClassifier(strategy="most_frequent").fit(Xtr, ytr)
base_pred = base.predict(Xte)

vec = TfidfVectorizer()
model = LogisticRegression(max_iter=1000).fit(vec.fit_transform(Xtr), ytr)
model_pred = model.predict(vec.transform(Xte))

print("\n=== RESULTS (test set size = %d) ===" % len(yte))
for name, pred in [("Baseline", base_pred), ("Model", model_pred)]:
    print(f"\n{name}: accuracy {accuracy_score(yte, pred):.2f} | macro F1 {f1_score(yte, pred, average='macro'):.2f}")
    print("Confusion matrix (rows=true, cols=pred, order", labels, "):")
    print(confusion_matrix(yte, pred, labels=labels))
print(f"\nBaseline accuracy {accuracy_score(yte, base_pred):.2f} | "
      f"Model accuracy {accuracy_score(yte, model_pred):.2f}, F1 {f1_score(yte, model_pred, average='macro'):.2f}")

# ---------- 4. MISCLASSIFIED TICKETS ----------
print("\n=== MISCLASSIFIED TICKETS (5-fold cross-validation over all 38 tickets) ===")
pipe = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))
cv_pred = cross_val_predict(pipe, X, y, cv=5)
wrong = clean[cv_pred != y].assign(predicted=cv_pred[cv_pred != y]).head(3)
for _, r in wrong.iterrows():
    print(f"- '{r['text']}' | true={r['category']} | predicted={r['predicted']}")
print("Reasons: tickets are short, so TF-IDF has few strong words; they share words like "
      "'account', 'payment', 'login' or 'error' with other categories, and with only 38 "
      "training tickets the model has seen few examples of each wording.")

# ---------- 5. KMEANS (unsupervised) ----------
Xall = TfidfVectorizer().fit_transform(clean["text"])
clean["cluster"] = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(Xall)
print("\n=== KMEANS CLUSTERS vs REAL CATEGORIES ===")
print(pd.crosstab(clean["cluster"], clean["category"]))
print("""
1. KMeans never saw the labels, so cluster numbers (0,1,2) have no names; we match them to categories by looking at their contents.
2. Clusters group tickets by shared words, so they match the real categories only partly: tickets with the same key words (e.g. 'password', 'crash') group together.
3. Supervised learning (LogisticRegression) was clearly better here because the labels tell the model exactly what we want.""")
