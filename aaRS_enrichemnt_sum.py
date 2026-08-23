import pandas as pd

# Load the CSV file into a DataFrame
input_csv = '/Users/chintansoni/Desktop/NGS/CS_Vincent_DMS/BocK-H previous run/BocK-H_corr_noncM_PB.csv'

output_csv = '/Users/chintansoni/Desktop/NGS/CS_Vincent_DMS/BocK-H previous run/BocK-H_corr_noncM_PB_grouped.csv'
output2_csv = '/Users/chintansoni/Desktop/NGS/CS_Vincent_DMS/BocK-H previous run/BocK-H_corr_noncM_PB_avgd.csv'

df = pd.read_csv(input_csv)

# Group by 'aaRS' and aggregate the barcodes into a list
grouped_df = df.groupby('aaRS').agg(
    barcodes=('barcode', lambda x: list(x)),  # Create a list of barcodes for each aaRS
    rawbccountsin=('Rawbccounts_in', lambda y: list(y)),
    aaRS_count=('aaRS', 'size'),              # Count occurrences of each aaRS
    sum_average_ncAA=('average_ncAA', 'sum'), # Sum of average_ncAA
    sum_average_noncAA=('average_noncAA', 'sum') # Sum of average_noncAA
).reset_index()

# Calculate the average values by dividing the sums by the count
grouped_df['average_ncAA'] = grouped_df['sum_average_ncAA'] / grouped_df['aaRS_count']
grouped_df['average_noncAA'] = grouped_df['sum_average_noncAA'] / grouped_df['aaRS_count']

# Save the grouped data to a new CSV file

grouped_df.to_csv(output_csv, index=False)

df2 = grouped_df[['aaRS', 'barcodes', 'rawbccountsin', 'aaRS_count', 'average_ncAA', 'average_noncAA']]

df2.to_csv(output2_csv, index = False)

print("Grouped data saved to", output_csv)
