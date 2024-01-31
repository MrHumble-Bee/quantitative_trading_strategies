import pandas as pd

# Assuming df is your DataFrame
# Replace this with your actual DataFrame
data = {'value': [10, 20, 30, 40]}
index_dates = pd.to_datetime(['2022-01-01', '2022-01-02', '2022-01-05', '2022-01-08'])
df = pd.DataFrame(data, index=index_dates)

# The target date you want to locate
target_date = pd.to_datetime('2022-01-04')

# Locate the target date or the next available date
try:
    loc = df.index.get_loc(target_date)
    found_date = df.index[loc]
except KeyError:
    loc = df.index.searchsorted(target_date)
    if loc == len(df.index):
        found_date = df.index[-1]  # Use the last date if target_date is beyond the last date
    else:
        found_date = df.index[loc]

print("Target Date:", target_date)
print("Found Date:", found_date)
