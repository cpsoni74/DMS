#Correction for 0 counts in output

import pandas as pd

# Read the file
df = pd.read_csv('/Users/chintansoni/Desktop/NGS/CS_Vincent_DMS/BocK-H previous run/BocK-H_10N1site Results.csv')

# Add 1 where out1 is 0
df.loc[df["out1"] == 0, "out1"] = 1
df.loc[df["out2"] == 0, "out2"] = 1

# Save the updated file
df.to_csv('/Users/chintansoni/Desktop/NGS/CS_Vincent_DMS/BocK-H previous run/BocK-H_10N1site Results_corr.csv', index=False)
