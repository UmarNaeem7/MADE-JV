from functools import reduce

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load the final_dfs from CSV
final_pm10_df = pd.read_csv("final_dfs/final_pm10_trends.csv")
final_pm2_df = pd.read_csv("final_dfs/final_pm2.5_trends.csv")
final_nox_df = pd.read_csv("final_dfs/final_nox_trends.csv")
final_nh3_df = pd.read_csv("final_dfs/final_nh3_trends.csv")
final_ch4_df = pd.read_csv("final_dfs/final_ch4_trends.csv")
final_hg_df = pd.read_csv("final_dfs/final_hg_trends.csv")
final_food_df = pd.read_csv("final_dfs/final_food_trends.csv")

# Add prefixes to each DataFrame's columns
final_pm10_df = final_pm10_df.add_prefix("PM10_")
final_pm2_df = final_pm2_df.add_prefix("PM2.5_")
final_nox_df = final_nox_df.add_prefix("NOx_")
final_nh3_df = final_nh3_df.add_prefix("NH3_")
final_ch4_df = final_ch4_df.add_prefix("CH4_")
final_hg_df = final_hg_df.add_prefix("Hg_")
final_food_df = final_food_df.add_prefix("Food_")

# Retain the 'Name' column as is
for df in [
    final_pm10_df,
    final_pm2_df,
    final_nox_df,
    final_nh3_df,
    final_ch4_df,
    final_hg_df,
    final_food_df,
]:
    df.rename(columns={df.columns[0]: "Name"}, inplace=True)


# List of prefixed DataFrames
dfs = [
    final_pm10_df,
    final_pm2_df,
    final_nox_df,
    final_nh3_df,
    final_ch4_df,
    final_hg_df,
    final_food_df,
]

# Merge all DataFrames on 'Name'
merged_df = reduce(lambda left, right: pd.merge(left, right, on="Name"), dfs)

print(merged_df.head())

## Perform correlataion
# Select relevant columns for correlation
correlation_columns = [col for col in merged_df.columns if "Percent_Change" in col]

# Compute correlation matrix
correlation_matrix = merged_df[correlation_columns].corr()

# Display correlation matrix
print(correlation_matrix)

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")

# Adjust labels
plt.xticks(rotation=0, fontsize=8)
plt.yticks(rotation=0)
plt.title("Correlation Heatmap", fontsize=16)
plt.tight_layout()

plt.show()
