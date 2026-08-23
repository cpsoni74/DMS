import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logomaker

# Define the WT sequence
WT_sequence = 'MMLARMSVYT'  # Replace with your actual WT sequence

def make_base_matrix_columns(sequences):
    columns = set()
    for x in sequences:
        columns.update(x)
    return sorted(columns)   

def populate_logo_matrix(sequences, quantifications, wt_sequence, columns=None):
    if columns is None:
        columns = make_base_matrix_columns(sequences)

    seq_len = len(sequences[0])
    ret = pd.DataFrame(np.zeros(shape=(seq_len, len(columns))),
                       index=list(range(seq_len)),
                       columns=columns)

    for s, q in zip(sequences, quantifications):
        if not np.isnan(q):
            for i, b in enumerate(s):
                if b != wt_sequence[i]:
                    ret.at[i, b] += q

    return ret

def make_logo_plot(fname, dat, width, height, font_size):
    seq_len = len(dat)
    x_labels = list(range(seq_len))

    # Create the logo plot
    logo = logomaker.Logo(dat, color_scheme='chemistry')
    logo.style_spines(visible=True, linewidth=4)
    logo.style_xticks(visible=False)
    logo.ax.set_xticks(range(seq_len))
    logo.ax.set_xticklabels(x_labels)
    logo.ax.set_ylabel('Weighted Enrichment Factor', fontsize=font_size)

    # Adjust plot to show negative values below 0 on the Y-axis
    min_value = dat.values.min()
    max_value = dat.values.max()
    logo.ax.set_ylim(min(min_value - 10 * abs(min_value), 0), max_value + 5 * abs(max_value))
    logo.style_glyphs_below(flip=False)

    # Manually set Y-axis tick labels with whole numbers
    y_ticks = np.arange(min(min_value - 10 * abs(min_value), 0), max_value + 5 * abs(max_value) + 1, 5)
    logo.ax.set_yticks(y_ticks)
    logo.ax.set_yticklabels([int(tick) if tick >= 0 else int(tick) for tick in y_ticks], fontsize=font_size)

    # Set the font size for X-axis tick labels
    for label in logo.ax.get_xticklabels():
        label.set_fontsize(font_size)

    plt.gcf().set_size_inches(width, height)
    plt.savefig(fname, format='svg', dpi=600)

# Read the CSV file
hits_df = pd.read_csv('/Users/chintansoni/Desktop/NGS/CS_Vincent_DMS/BocK-H previous run/BocK-H_corr_aaRS_log2en.csv')

# Print the column names to debug
print("Column names:", hits_df.columns)

# Use the correct column names for sequences and quantifications
sequences = hits_df['aaRS']
quantifications = hits_df['Log2_en']  # Adjust this if needed based on actual column name

col = make_base_matrix_columns(sequences)
df = populate_logo_matrix(sequences, quantifications, WT_sequence, col)

# Save the matrix to a CSV file (optional)
df.to_csv('/Users/chintansoni/Desktop/NGS/CS_Vincent_DMS/BocK-H previous run/BocK-H_corr_aaRS_log2en_mod.csv')

# Generate and save the WebLogo
make_logo_plot('/Users/chintansoni/Desktop/NGS/CS_Vincent_DMS/BocK-H previous run/BocK-H_corr_aaRS_log2en_VAMP.svg', df, 30, 30, 50)
