# Technical Proposal: Contract Q&A Assistant (60-page contracts)

**Prepared by:** Yoho | **Client:** Mid-size company

## 1. Problem
Staff spend hours searching long contracts for answers (notice period, penalties, renewal terms). We propose an assistant that answers questions in seconds and shows the exact clause.

## 2. Recommended approach: RAG (Retrieval-Augmented Generation)
1. Convert the PDF to text and split it into small chunks by clause/section (about 300 to 500 words, with overlap).
2. Create an embedding for each chunk and store them in a vector store.
3. For each question, retrieve the top 3 to 5 most similar chunks (cosine similarity).
4. Send only those chunks to an LLM with the instruction: *answer only from this text, cite the clause, say "not found" if unsure* (temperature 0).
5. Show the answer with the clause number, and flag low-confidence answers for legal review.

## 3. Data requirements
- 20 to 50 contracts as text-based PDFs (OCR needed for scans).
- A test set of 50 questions with correct answers and clause numbers, written by the legal team.
- Access control: contracts are confidential and stay in the company's environment.

## 4. Evaluation metric and target
- **Answer accuracy ≥ 90%** on the 50-question test set (judged correct by a lawyer).
- **100% of answers must cite a clause**, and hallucination rate (made-up clauses) **< 2%**.
- Response time under 5 seconds.

## 5. Estimated build time
About **3 weeks**: week 1 data preparation and chunking, week 2 build the RAG pipeline, week 3 testing, tuning and demo.

## 6. Key trade-offs
- **Accuracy vs cost:** more retrieved chunks improve accuracy but increase tokens and cost.
- **Speed vs quality:** a larger model is better but slower and more expensive.
- **Risk:** retrieval can miss a clause, so a human (legal) must review important answers; this is an assistant, not legal advice.
- **Privacy:** an approved, private LLM deployment is required for confidential contracts.

## Why not just ask ChatGPT?
1. **Confidentiality:** pasting contracts into a public tool risks leaking private data.
2. **Hallucination:** a general chatbot may invent clauses and gives no reliable source; our system answers only from the contract and cites it.
3. **Control and measurement:** we can test accuracy, set a target and monitor it; with ChatGPT we cannot.
4. **Scale:** a 60-page contract plus many contracts do not fit well in a chat window; retrieval finds the right part automatically.
