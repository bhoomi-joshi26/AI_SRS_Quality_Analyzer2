import pandas as pd
import random

# -----------------------------------
# Lists for generating requirements
# -----------------------------------

users = [
    "customers",
    "administrators",
    "employees",
    "registered users",
    "system operators"
]

actions = [
    "login into the system",
    "upload documents",
    "manage user accounts",
    "generate reports",
    "process transactions",
    "update profile information",
    "search records",
    "track activities"
]

methods = [
    "secure authentication",
    "OTP verification",
    "password validation",
    "role based access control",
    "multi factor authentication"
]

features = [
    "notification",
    "backup",
    "search",
    "authentication",
    "monitoring",
    "report generation",
    "data management"
]

security = [
    "AES encryption",
    "secure database storage",
    "access control mechanism",
    "encrypted communication"
]

data_types = [
    "customer information",
    "transaction details",
    "employee records",
    "system logs",
    "user credentials"
]

time_values = [
    2,
    3,
    5,
    8,
    10
]


# -----------------------------------
# High Quality Requirements
# -----------------------------------

high_quality = []

counter = 1


for i in range(500):

    sentence = (
        f"The system shall allow {random.choice(users)} "
        f"to {random.choice(actions)} "
        f"using {random.choice(methods)}. "
        f"The system shall process requests within "
        f"{random.choice(time_values)} seconds "
        f"and store {random.choice(data_types)} "
        f"using {random.choice(security)}."
    )


    sentence += f" Requirement Number {counter}"

    high_quality.append(
        [
            sentence,
            "High"
        ]
    )

    counter += 1



# -----------------------------------
# Low Quality Requirements
# -----------------------------------

low_words = [
    "fast",
    "better",
    "simple",
    "easy",
    "good",
    "efficient",
    "proper",
    "advanced"
]


low_quality = []


for i in range(2000):

    sentence = (
        f"The system should be {random.choice(low_words)} "
        f"and should provide good performance. "
        f"The application should work properly "
        f"according to user needs."
    )


    sentence += f" Requirement Number {counter}"


    low_quality.append(
        [
            sentence,
            "Low"
        ]
    )

    counter += 1



# -----------------------------------
# Combine Dataset
# -----------------------------------

dataset = high_quality + low_quality


random.shuffle(dataset)



df = pd.DataFrame(
    dataset,
    columns=[
        "requirement",
        "label"
    ]
)



# -----------------------------------
# Remove duplicates
# -----------------------------------

df.drop_duplicates(
    subset="requirement",
    inplace=True
)



# -----------------------------------
# Save Dataset
# -----------------------------------

df.to_csv(
    "srs_dataset.csv",
    index=False
)



print(
    "Dataset Created Successfully!"
)


print(
    "Total Samples:",
    len(df)
)


print(df.head())