# Re-import required library
import matplotlib.pyplot as plt

# Cleaned competing factors and scores
factors_cleaned = [
    "Cost of Access", "Content Variety", "Speed of Information", "Credibility",
    "Depth of Content", "Interactivity", "Personalization",
    "Ad-Free Experience", "User-Generated Content"
]

# Offering levels (1 = Low, 5 = High)
twitter_scores_cleaned = [1, 5, 5, 1, 2, 5, 5, 2, 5]
nyt_scores_cleaned = [5, 4, 3, 5, 5, 2, 2, 4, 1]

# Create the updated plot
plt.figure(figsize=(12, 6))
plt.plot(factors_cleaned, twitter_scores_cleaned, label="Twitter", marker="o", linestyle="-", linewidth=2)
plt.plot(factors_cleaned, nyt_scores_cleaned, label="The New York Times", marker="o", linestyle="--", linewidth=2)

# Add labels and title
plt.title("Blue Ocean Strategy Canvas: Twitter vs. The New York Times (Traditional Media)", fontsize=16)
plt.xlabel("Competing Factors", fontsize=12)
plt.ylabel("Offering Level (1 = Low, 5 = High)", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(range(1, 6), fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.legend(fontsize=12)

# Display the updated plot
plt.tight_layout()
plt.show()
