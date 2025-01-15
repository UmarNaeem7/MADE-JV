import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

file_path = "../../data/EDGAR_NH3_1970_2022.xlsx"

# Read the Excel file, skipping the first 9 rows
df = pd.read_excel(file_path, sheet_name="TOTALS BY COUNTRY", skiprows=9)

countries_list = [
    "United States",
    "Argentina",
    "Mexico",
    "Brazil",
    "Chile",
    "Venezuela",
    "Canada",
]

groups_list = [
    "Rest Central America",
    "Rest South America",
    "USA",
    "Mexico",
    "Brazil",
    "Canada",
]

filtered_df = df[df["C_group_IM24_sh"].isin(groups_list)]

trends_df = pd.DataFrame()
trends_df[["Name", "Y_2022"]] = filtered_df[["Name", "Y_2022"]]

# Calculate trend metrics

# 1. Percent Change
trends_df["Percent_Change"] = (
    (filtered_df["Y_2022"] - filtered_df["Y_1970"]) / filtered_df["Y_1970"]
) * 100

# 2. Absolute Change
trends_df["Absolute_Change"] = filtered_df["Y_2022"] - filtered_df["Y_1970"]

# 3. Average Annual Change
trends_df["Annual_Change"] = trends_df["Absolute_Change"] / (2022 - 1970)

# 4. Volatility (Standard Deviation)
trends_df["Volatility"] = filtered_df.loc[:, "Y_1970":"Y_2022"].std(axis=1)

# 5. Linear Trend (Slope)
years = np.array(
    [int(col[2:]) for col in filtered_df.columns if col.startswith("Y_")]
).reshape(-1, 1)
slopes = []

for index, row in filtered_df.iterrows():
    nh3_values = row.loc["Y_1970":"Y_2022"].values.reshape(-1, 1)
    model = LinearRegression()
    model.fit(years, nh3_values)
    slopes.append(model.coef_[0][0])  # Store slope (rate of change per year)

trends_df["Linear_Trend_Slope"] = slopes

# 6. Max and Min NH3 Values and Their Years
trends_df["Max_NH3_Year"] = filtered_df.loc[:, "Y_1970":"Y_2022"].idxmax(axis=1)
trends_df["Min_NH3_Year"] = filtered_df.loc[:, "Y_1970":"Y_2022"].idxmin(axis=1)

# 7. Latest Year Contribution (Percent of Total)
total_2022 = filtered_df["Y_2022"].sum()
trends_df["Contribution_2022"] = (filtered_df["Y_2022"] / total_2022) * 100

# only include prominent countries in final df
final_df = trends_df[trends_df["Name"].isin(countries_list)]
print(final_df.head(n=10))


# Plotting
plt.figure(figsize=(12, 6))
plt.plot(
    final_df["Name"], final_df["Percent_Change"], marker="o", linestyle="-", color="b"
)

# Add title and labels
plt.title("Percent Change of NH3 from 1975 to 2022 by Country", fontsize=14)
plt.xlabel("Country", fontsize=12)
plt.ylabel("Percent Change", fontsize=12)

# Display the plot
plt.tight_layout()
plt.show()

# bar chart for contributions
plt.figure(figsize=(12, 6))
plt.bar(final_df["Name"], final_df["Contribution_2022"], color="c")

# Add title and labels
plt.title("Contribution of Each Country to Total NH3 in Americas in 2022", fontsize=14)
plt.xlabel("Country", fontsize=12)
plt.ylabel("Contribution in 2022 (%)", fontsize=12)

# Display the plot
plt.tight_layout()
plt.show()

final_df.to_csv("./final_dfs/final_nh3_trends.csv", index=False)
