# Data file: 12 FAQ questions (HR, IT, payroll) + test queries

FAQS = [
    # (id, department, question, short answer)
    ("IT-1", "IT", "How do I reset my password if I am locked out of my account?",
     "Use the self-service portal or contact the IT helpdesk."),
    ("IT-2", "IT", "How do I connect to the office VPN from outside?",
     "Install the VPN client and sign in with your company ID."),
    ("IT-3", "IT", "How can I request a new laptop or replacement equipment?",
     "Raise an equipment request ticket with manager approval."),
    ("IT-4", "IT", "Who do I contact when the printer or Wi-Fi stops working?",
     "Call the IT helpdesk extension 100."),
    ("HR-1", "HR", "What are the rules for working from home or remote work?",
     "Employees may work remotely up to 2 days a week with manager approval."),
    ("HR-2", "HR", "How many days of annual leave am I entitled to each year?",
     "Full-time employees get 20 days of annual leave."),
    ("HR-3", "HR", "How do I apply for sick leave or medical leave?",
     "Inform your manager and submit the leave form in the HR portal."),
    ("HR-4", "HR", "What is the process for submitting my resignation?",
     "Send a written notice to your manager and HR."),
    ("PAY-1", "Payroll", "On which date are monthly wages deposited into my bank account?",
     "Wages are paid on the last working day of each month."),
    ("PAY-2", "Payroll", "How can I download my payslip?",
     "Payslips are available in the payroll portal under Documents."),
    ("PAY-3", "Payroll", "How do I update my bank details for payments?",
     "Submit the bank change form to payroll before the 20th."),
    ("PAY-4", "Payroll", "How are income tax deductions and reimbursements calculated?",
     "Tax is deducted per the declared investment plan; claims are reimbursed monthly."),
]

# (query, id of the FAQ that is the correct answer, why semantic search should handle it)
TEST_QUERIES = [
    ("I cannot log in", "IT-1",
     "The query says 'log in' but the FAQ says 'password' and 'locked out'. They share no words, "
     "yet embeddings place both near the idea of an access/login problem."),
    ("when is salary credited", "PAY-1",
     "The FAQ uses 'wages' and 'deposited' instead of 'salary' and 'credited'. Keyword search finds "
     "no common word; embeddings treat these synonyms as close in meaning."),
    ("work from home rules", "HR-1",
     "Here the query and the FAQ share the words 'home' and 'rules', so keyword search also works."),
]