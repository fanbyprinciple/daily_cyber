import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Load CSV
df = pd.read_csv('/content/Abstract excel sccs.csv')

# Step 2: Filter the data for 'C' and 'T'
df_C = df[df['Control/Test'] == 'C']
df_T = df[df['Control/Test'] == 'T']

print(len(df_C['Bottom Left corner']))
print(len(df_T['Bottom Left corner']))



# Step 3: Prepare the data for Seaborn by combining 'C' and 'T' into a single DataFrame
combined_df = pd.DataFrame({
    'Bottom Left Corner': pd.concat([df_C['Bottom Left corner'], df_T['Bottom Left corner']]),
    'Bottom Right Corner': pd.concat([df_C['Bottom Right Corner'], df_T['Bottom Right Corner']]),
    'Top Left Corner': pd.concat([df_C['Top Left Corner'], df_T['Top Left Corner']]),
    'Top Right Corner': pd.concat([df_C['Top Right Corner'], df_T['Top Right Corner']]),
    'Group': ['C'] * len(df_C) + ['T'] * len(df_T)  # Add a column to distinguish between 'C' and 'T'
})

# Step 4: Create a figure with separate subplots for each corner
fig, axes = plt.subplots(1, 4, figsize=(16, 8), sharey=True)

# Plot for Bottom Left Corner
sns.boxplot(x='Group', y='Bottom Left Corner', data=combined_df, palette=["#FF6347", "#4682B4"], ax=axes[0])
axes[0].set_title('Bottom Left Corner')

# Plot for Bottom Right Corner
sns.boxplot(x='Group', y='Bottom Right Corner', data=combined_df, palette=["#32CD32", "#FFD700"], ax=axes[1])
axes[1].set_title('Bottom Right Corner')

# Plot for Top Left Corner
sns.boxplot(x='Group', y='Top Left Corner', data=combined_df, palette=["#FF6347", "#4682B4"], ax=axes[2])
axes[2].set_title('Top Left Corner')

# Plot for Top Right Corner
sns.boxplot(x='Group', y='Top Right Corner', data=combined_df, palette=["#32CD32", "#FFD700"], ax=axes[3])
axes[3].set_title('Top Right Corner')

# Step 5: Add a shared y-axis label and a main title
fig.supylabel('Values')
fig.suptitle('Side-by-Side Boxplots for C and T')

# Step 6: Add a legend that maps colors to the columns (Bottom Left Corner, Bottom Right Corner, etc.)
handles = [
    plt.Line2D([0], [0], color="#FF6347", lw=4, label='Bottom Left Corner'),
    plt.Line2D([0], [0], color="#32CD32", lw=4, label='Bottom Right Corner'),
    plt.Line2D([0], [0], color="#4682B4", lw=4, label='Top Left Corner'),
    plt.Line2D([0], [0], color="#FFD700", lw=4, label='Top Right Corner')
]
fig.legend(handles=handles, title='Corners', loc='upper right')

# Step 7: Show the plot
plt.tight_layout()
plt.show()