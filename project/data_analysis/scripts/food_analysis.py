import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

file_path = "../../data/EDGAR-FOOD_v61_AP.xlsx"

# Read the Excel file, skipping the first 3 rows
df = pd.read_excel(file_path, sheet_name="Suppl. Table 4-Emi by Country", skiprows=3)

countries_list = [
    "United States",
    "Argentina",
    "Mexico",
    "Brazil",
    "Chile",
    "Venezuela",
    "Canada",
]

filtered_df = df[df["Name"].isin(countries_list)]

years = [year for year in range(1970, 2019)]  # List of years from 1970 to 2018

# Group by Name & sum all the yearly columns
aggregated_df = filtered_df.groupby("Name")[years].sum().reset_index()
aggregated_df = aggregated_df.reset_index()

trends_df = pd.DataFrame()
trends_df[["Name", 2018]] = aggregated_df[["Name", 2018]]

# Calculate trend metrics
# 1. Percent Change
trends_df["Percent_Change"] = (
    (aggregated_df[2018] - aggregated_df[1970]) / aggregated_df[1970]
) * 100

# 2. Absolute Change
trends_df["Absolute_Change"] = aggregated_df[2018] - aggregated_df[1970]

# 3. Average Annual Change
trends_df["Annual_Change"] = trends_df["Absolute_Change"] / (2018 - 1970)

# 4. Volatility (Standard Deviation)
trends_df["Volatility"] = aggregated_df.loc[:, 1970:2018].std(axis=1)

# 5. Linear Trend (Slope)
years = np.arange(1970, 2019).reshape(-1, 1)
slopes = []

for index, row in aggregated_df.iterrows():
    food_values = row.loc[1970:2018].values.reshape(-1, 1)
    model = LinearRegression()
    model.fit(years, food_values)
    slopes.append(model.coef_[0][0])  # Store slope (rate of change per year)

trends_df["Linear_Trend_Slope"] = slopes

# 6. Max and Min Food Values and Their Years
trends_df["Max_Food_Year"] = aggregated_df.loc[:, 1970:2018].idxmax(axis=1)
trends_df["Min_Food_Year"] = aggregated_df.loc[:, 1970:2018].idxmin(axis=1)

# 7. Latest Year Contribution (Percent of Total)
total_2018 = aggregated_df[2018].sum()
trends_df["Contribution_2018"] = (aggregated_df[2018] / total_2018) * 100
# print("Trends df:")
print(trends_df)


# Plotting
plt.figure(figsize=(12, 6))
plt.plot(
    trends_df["Name"], trends_df["Percent_Change"], marker="o", linestyle="-", color="b"
)

# Add title and labels
plt.title("Percent Change of Food Emissions from 1975 to 2018 by Country", fontsize=14)
plt.xlabel("Country", fontsize=12)
plt.ylabel("Percent Change", fontsize=12)

# Display the plot
plt.tight_layout()
plt.show()

# bar chart for contributions
plt.figure(figsize=(12, 6))
plt.bar(trends_df["Name"], trends_df["Contribution_2018"], color="c")

# Add title and labels
plt.title(
    "Contribution of Each Country to Total Food Emissions in Americas in 2018",
    fontsize=14,
)
plt.xlabel("Country", fontsize=12)
plt.ylabel("Contribution in 2018 (%)", fontsize=12)

# Display the plot
plt.tight_layout()
plt.show()

trends_df.to_csv("./final_dfs/final_food_trends.csv", index=False)
