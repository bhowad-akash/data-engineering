import sys
import pandas as pd

df = pd.DataFrame({'month': [1, 2, 3], 'value': [10, 20, 30]})
print(df)

print("arguments:", sys.argv)
month = int(sys.argv[1])
print("Hey folks!", f"Running pipeline for month {month}")

df.to_parquet(f"output_day_{sys.argv[1]}.parquet")