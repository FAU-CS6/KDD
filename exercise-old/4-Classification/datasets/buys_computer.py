import pandas as pd


train_buys_computer = pd.DataFrame(
    [
        ["<=30", "high", "no", "fair", "no"],
        ["<=30", "high", "no", "excellent", "no"],
        ["31-40", "high", "no", "fair", "yes"],
        [">40", "medium", "no", "fair", "yes"],
        [">40", "low", "yes", "fair", "yes"],
        [">40", "low", "yes", "excellent", "no"],
        ["31-40", "low", "yes", "excellent", "yes"],
        ["<=30", "medium", "no", "fair", "no"],
        ["<=30", "low", "yes", "fair", "yes"],
        [">40", "medium", "yes", "fair", "yes"],
        ["<=30", "medium", "yes", "excellent", "yes"],
        ["31-40", "medium", "no", "excellent", "yes"],
        ["31-40", "high", "yes", "fair", "yes"],
        [">40", "medium", "no", "excellent", "no"],
    ],
    columns=["age", "income", "student", "credit_rating", "buys_computer"],
)

test_buys_computer = pd.DataFrame(
    [["<=30", "medium", "yes", "fair", "yes"]],
    columns=["age", "income", "student", "credit_rating", "buys_computer"],
)
