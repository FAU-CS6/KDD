import pandas as pd


orders = pd.DataFrame(
    data={
        "OID": list(range(1, 11)),
        "CID": [2, 2, 2, 4, 1, 9, 7, 7, 7, 7],
        "DATE": pd.date_range(start="2022-03-25", periods=10),
    }
)
