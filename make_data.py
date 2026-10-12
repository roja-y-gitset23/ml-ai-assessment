"""Creates tickets_raw.csv: 46 rows = 38 unique + 3 duplicates (casing differs)
+ 2 duplicates with blank category + 3 rows with missing values."""
import pandas as pd

billing = [
 "I was charged twice for my subscription this month",
 "Please send me an invoice for last month's payment",
 "My refund has not arrived yet",
 "The credit card payment failed but money was deducted",
 "How do I update my billing address on the invoice",
 "I want to cancel my plan and get a refund",
 "Why is my bill higher than usual this month",
 "Discount coupon was not applied to my payment",
 "I need a receipt for my last transaction",
 "Wrong amount charged on my credit card",
 "Can I change my payment method to a different card",
 "Tax is missing on my invoice",
]
technical = [
 "The app crashes every time I open the dashboard",
 "Error 500 appears when I upload a file",
 "The website is very slow and pages do not load",
 "Software crashes after the latest update",
 "I get a server error when I click submit",
 "The mobile app freezes on the home screen",
 "Report export fails with an unknown error",
 "Page shows blank screen after loading",
 "Notifications are not working on my phone app",
 "Bug in the search feature returns no results",
 "Upload keeps failing with a timeout error",
 "The system is down and I cannot load anything",
 "Video player keeps buffering and then crashes",
 "API returns an error code when I send a request",
]
account = [
 "I forgot my password and cannot log in",
 "Please reset my password",
 "My account is locked after too many login attempts",
 "How do I change the email address on my account",
 "I want to delete my account permanently",
 "Cannot sign in to my profile",
 "Update my name and phone number in my profile",
 "I did not receive the verification email for my account",
 "Please enable two factor login for my account",
 "Username change request for my profile",
 "Unable to log in with my registered email",
 "Add a new user to my account",
]
rows = [(t, "Billing") for t in billing] + [(t, "Technical") for t in technical] + [(t, "Account") for t in account]
assert len(rows) == 38

# inconsistent casing (original rows)
rows[0] = (rows[0][0].upper(), "billing")
rows[14] = (rows[14][0].lower(), "TECHNICAL")
rows[30] = (rows[30][0], "account")

dups_case = [(rows[1][0].lower(), rows[1][1]), (rows[15][0].upper(), rows[15][1]), (rows[31][0], rows[31][1])]
dups_blank = [(rows[2][0], None), (rows[16][0], None)]
missing = [(None, "Billing"), (None, "Technical"), ("Need help with something on my page", None)]
raw = rows + dups_case + dups_blank + missing
assert len(raw) == 46
df = pd.DataFrame(raw, columns=["text", "category"])
df = df.sample(frac=1, random_state=1).reset_index(drop=True)
df.to_csv("tickets_raw.csv", index=False)
print("tickets_raw.csv rows:", len(df))
