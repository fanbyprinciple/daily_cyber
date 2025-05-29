
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import uuid

# Function to split and clean author and institution lists
def split_and_clean(column_data):
    items = []
    for entry in column_data.dropna():
        # Split by commas and clean whitespace
        split_items = [item.strip() for item in entry.split(',')]
        items.extend(split_items)
    return [item for item in items if item]  # Remove empty strings

# Load Sheet 2 from the Excel file
try:
    df = pd.read_excel('ayana.xlsx', sheet_name=1)  # Sheet 2 (index 1)
except FileNotFoundError:
    try:
        # Fallback for loadFileData if file is not local
        csv_data = loadFileData('ayana.xlsx')
        df = pd.read_csv(pd.StringIO(csv_data))
    except NameError:
        raise Exception("File 'ayana.xlsx' not found and loadFileData not defined. Please provide the file or define loadFileData.")
except Exception as e:
    raise Exception(f"Error loading file: {str(e)}")

# Verify required columns exist
required_columns = ['Authors', 'Institutions', 'Journal']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# Extract relevant columns
authors = df['Authors']
institutions = df['Institutions']
journals = df['Journal']

# Count occurrences
author_counts = Counter(split_and_clean(authors))
institution_counts = Counter(split_and_clean(institutions))
journal_counts = Counter(journals.dropna())

# Get top 5 for each category
top_authors = author_counts.most_common(5)
top_institutions = institution_counts.most_common(5)
top_journals = journal_counts.most_common(5)

# Prepare data for plotting
author_names, author_freq = zip(*top_authors) if top_authors else ([], [])
inst_names, inst_freq = zip(*top_institutions) if top_institutions else ([], [])
journal_names, journal_freq = zip(*top_journals) if top_journals else ([], [])

# Create a figure with three subplots
plt.style.use('fivethirtyeight')  # Sleek, modern style
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

# Color scheme
base_color = '#1f77b4'  # Blue for bars
highlight_color = '#ffd700'  # Gold for top entity
colors_authors = [highlight_color if i == 0 else base_color for i in range(len(author_names))]
colors_insts = [highlight_color if i == 0 else base_color for i in range(len(inst_names))]
colors_journals = [highlight_color if i == 0 else base_color for i in range(len(journal_names))]

# Plot Authors
bars1 = ax1.bar(author_names, author_freq, color=colors_authors, edgecolor='black')
ax1.set_title('Top 5 Authors by Publication Count', fontsize=14, pad=10)
ax1.set_xlabel('Authors', fontsize=12)
ax1.set_ylabel('Number of Publications', fontsize=12)
ax1.tick_params(axis='x', rotation=45, labelsize=10)
ax1.grid(True, axis='y', linestyle='--', alpha=0.7)

# Annotate the top author
if author_freq:
    max_author_idx = np.argmax(author_freq)
    ax1.text(max_author_idx, author_freq[max_author_idx] + 0.2, 
             f'{author_names[max_author_idx]}\n({author_freq[max_author_idx]})', 
             ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

# Plot Institutions
bars2 = ax2.bar(inst_names, inst_freq, color=colors_insts, edgecolor='black')
ax2.set_title('Top 5 Institutions by Publication Count', fontsize=14, pad=10)
ax2.set_xlabel('Institutions', fontsize=12)
ax2.tick_params(axis='x', rotation=45, labelsize=10)
ax2.grid(True, axis='y', linestyle='--', alpha=0.7)

# Annotate the top institution
if inst_freq:
    max_inst_idx = np.argmax(inst_freq)
    ax2.text(max_inst_idx, inst_freq[max_inst_idx] + 0.2, 
             f'{inst_names[max_inst_idx]}\n({inst_freq[max_inst_idx]})', 
             ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

# Plot Journals
bars3 = ax3.bar(journal_names, journal_freq, color=colors_journals, edgecolor='black')
ax3.set_title('Top 5 Journals by Publication Count', fontsize=14, pad=10)
ax3.set_xlabel('Journals', fontsize=12)
ax3.tick_params(axis='x', rotation=45, labelsize=10)
ax3.grid(True, axis='y', linestyle='--', alpha=0.7)

# Annotate the top journal
if journal_freq:
    max_journal_idx = np.argmax(journal_freq)
    ax3.text(max_journal_idx, journal_freq[max_journal_idx] + 0.2, 
             f'{journal_names[max_journal_idx]}\n({journal_freq[max_journal_idx]})', 
             ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

# Adjust layout and styling
plt.tight_layout()
fig.suptitle('Top Authors, Institutions, and Journals for Mahseer Research', fontsize=16, y=1.05)
fig.patch.set_facecolor('#f0f0f0')  # Light grey background for sleek look

# Save the plot
plt.savefig('top_entities_plot.png', dpi=300, bbox_inches='tight')
plt.close()
