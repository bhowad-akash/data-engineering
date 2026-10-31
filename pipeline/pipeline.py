import sys
import pandas as pd

print("hello Akash")
month = sys.argv[1]
print(f"Running pipeline for the month of {month}")

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
})

print("DataFrame created:")
print(df)

df.to_parquet(f"data_{month}.parquet", engine='pyarrow', index=False)
print(f"DataFrame saved to data_{month}.parquet")