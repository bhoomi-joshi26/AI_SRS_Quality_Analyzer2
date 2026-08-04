import random
from pathlib import Path
import pandas as pd

random.seed(42)

out_dir = Path("dataset")
out_dir.mkdir(parents=True, exist_ok=True)

high_quality = [
    "The user shall log in using a username and password.",
    "The application shall encrypt all user passwords before storage.",
    "The system shall generate monthly sales reports in PDF format.",
    "The interface shall display an error message when login fails.",
    "The system shall allow an administrator to reset a user password.",
    "The application shall log each successful login with a timestamp.",
    "The system shall validate that the email address is in a correct format.",
    "The system shall save user profile changes within 5 seconds.",
    "The application shall allow users to upload files up to 20 MB.",
    "The system shall send a password reset link to the registered email address.",
    "The system shall support concurrent access by at least 100 users.",
    "The application shall store audit logs for 12 months.",
    "The interface shall provide a search field on the dashboard page.",
    "The system shall calculate the total order amount before checkout.",
    "The application shall require two-factor authentication for admin access.",
    "The system shall prevent access to disabled user accounts.",
    "The application shall generate a confirmation email after registration.",
    "The system shall display order history for the last 6 months.",
    "The system shall complete a database backup every night at 2:00 AM.",
    "The application shall export user data to a CSV file."
]

low_quality = [
    "The system should be fast.",
    "The interface should be user-friendly.",
    "The software should work properly.",
    "The application should be secure.",
    "The system should respond quickly.",
    "The product should be easy to use.",
    "The application should have a nice design.",
    "The system should perform well under heavy load.",
    "The software should be reliable.",
    "The interface should look modern.",
    "The application should not crash.",
    "The system should support many users.",
    "The software should be efficient.",
    "The system should be scalable.",
    "The application should be intuitive.",
    "The interface should be simple.",
    "The system should be stable.",
    "The software should be easy to maintain.",
    "The application should be compatible with browsers.",
    "The system should have good performance."
]

rows = []

for _ in range(3000):
    rows.append({
        "requirement": random.choice(high_quality),
        "label": 1
    })

for _ in range(3000):
    rows.append({
        "requirement": random.choice(low_quality),
        "label": 0
    })

random.shuffle(rows)

df = pd.DataFrame(rows, columns=["requirement", "label"])
df.to_csv(out_dir / "srs_dataset.csv", index=False, encoding="utf-8")
print("Saved:", out_dir / "srs_dataset.csv")
print("Rows:", len(df))
print(df["label"].value_counts().to_dict())