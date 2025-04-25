import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# Load game data
with open("last_100_chess_games.json", "r") as f:
    games = json.load(f)

# Extract relevant fields
data = []
for game in games:
    color = "White" if game["white"]["username"].lower() == "samuraibartu" else "Black"
    result = game["white"]["result"] if color == "White" else game["black"]["result"]
    my_rating = game["white"]["rating"] if color == "White" else game["black"]["rating"]
    opponent_rating = game["black"]["rating"] if color == "White" else game["white"]["rating"]
    data.append({
        "Date": pd.to_datetime(game["end_time"], unit="s"),
        "Time Control": game.get("time_control"),
        "Time Class": game.get("time_class"),
        "Result": result,
        "My Color": color,
        "My Rating": my_rating,
        "Opponent Rating": opponent_rating,
        "Opponent Username": game["black"]["username"] if color == "White" else game["white"]["username"],
        "URL": game.get("url")
    })

# Create DataFrame
df = pd.DataFrame(data)
df["Rating Diff"] = df["My Rating"] - df["Opponent Rating"]
df["Win"] = df["Result"].apply(lambda x: 1 if x == "win" else 0)

# Save cleaned data
df.to_csv("cleaned_chess_data.csv", index=False)

# Plot 1: Win Rate by Color
sns.set(style="whitegrid")
plt.figure(figsize=(6, 4))
sns.barplot(data=df, x="My Color", y="Win")
plt.title("Win Rate by Color")
plt.tight_layout()
plt.savefig("win_rate_by_color.png")
plt.close()

# Plot 2: Rating Difference Distribution
plt.figure(figsize=(6, 4))
sns.histplot(df["Rating Diff"], bins=20, kde=True)
plt.title("Rating Difference Distribution")
plt.tight_layout()
plt.savefig("rating_diff_distribution.png")
plt.close()

# Plot 3: Win Rate by Time Control
plt.figure(figsize=(8, 4))
sns.barplot(data=df, x="Time Control", y="Win")
plt.xticks(rotation=45)
plt.title("Win Rate by Time Control")
plt.tight_layout()
plt.savefig("win_rate_by_time_control.png")
plt.close()

# Hypothesis Testing
greater = df[df["Rating Diff"] > 0]["Win"]
less_equal = df[df["Rating Diff"] <= 0]["Win"]
t_stat, p_val = ttest_ind(greater, less_equal)

print("T-test results:")
print("T-statistic:", round(t_stat, 3))
print("P-value:", round(p_val, 5))
