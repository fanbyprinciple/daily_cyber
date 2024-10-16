!pip install pandas matplotlib seaborn

import pandas as pd

# Load CSV into DataFrame
df = pd.read_csv('/content/Abstract excel sccs.csv')

import seaborn as sns

# Step 2: Create a figure with 4 subplots
fig, axes = plt.subplots(1, 4, figsize=(16, 6), sharey=True)

filtered_df = df[df['Control/Test'] == 'C']

# Step 3: Create boxplots on each subplot with different colors
sns.boxplot(data=filtered_df['Bottom Left corner'], ax=axes[0], color="#FF6347")
axes[0].set_title('Bottom Left corner')
axes[0].set_xlabel('Control')

sns.boxplot(data=filtered_df['Bottom Right Corner'], ax=axes[1], color="#4682B4")
axes[1].set_title('Bottom Right Corner')
axes[1].set_xlabel('Control')

sns.boxplot(data=filtered_df['Top Left Corner'], ax=axes[2], color="#32CD32")
axes[2].set_title('Top Left Corner')
axes[2].set_xlabel('Control')

sns.boxplot(data=filtered_df['Top Right Corner'], ax=axes[3], color="#FFD700")
axes[3].set_title('Top Right Corner')
axes[3].set_xlabel('Control')

# Step 4: Adjust layout
plt.tight_layout()

# Step 5: Show plot
plt.show()

# Step 2: Create a figure with 4 subplots
fig, axes = plt.subplots(1, 4, figsize=(16, 6), sharey=True)

filtered_df = df[df['Control/Test'] == 'T']

# Step 3: Create boxplots on each subplot with different colors
sns.boxplot(data=filtered_df['Bottom Left corner'], ax=axes[0], color="#FF6347")
axes[0].set_title('Bottom Left corner')
axes[0].set_xlabel('Test')

sns.boxplot(data=filtered_df['Bottom Right Corner'], ax=axes[1], color="#4682B4")
axes[1].set_title('Bottom Right Corner')
axes[1].set_xlabel('Test')

sns.boxplot(data=filtered_df['Top Left Corner'], ax=axes[2], color="#32CD32")
axes[2].set_title('Top Left Corner')
axes[2].set_xlabel('Test')

sns.boxplot(data=filtered_df['Top Right Corner'], ax=axes[3], color="#FFD700")
axes[3].set_title('Top Right Corner')
axes[3].set_xlabel('Test')

# Step 4: Adjust layout
plt.tight_layout()

# Step 5: Show plot
plt.show()

