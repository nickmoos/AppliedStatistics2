import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from statsmodels.stats.proportion import proportion_confint

# data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech_Copy.csv")
data = pd.DataFrame({
    'How satisfied are you with your product A': [5]*17 + [4]*6 + [3]*3 + [1]*1
})


def satisfaction_pie():
    satisfaction_columns = [col for col in data.columns if col.startswith('How satisfied are you with your')]

    # Calculate the average satisfaction score for each respondent
    data['Overall Satisfaction'] = data[satisfaction_columns].mean(axis=1).round()

    # Map numerical scores to textual labels
    satisfaction_labels = {
        1.0: 'Very Dissatisfied',
        2.0: 'Dissatisfied',
        3.0: 'Neutral',
        4.0: 'Satisfied',
        5.0: 'Very Satisfied'
    }
    data['Overall Satisfaction Label'] = data['Overall Satisfaction'].map(satisfaction_labels)

    # Count the occurrences of each satisfaction level
    satisfaction_counts = data['Overall Satisfaction Label'].value_counts()

    # Calculate the percentage for each slice to determine explosion
    satisfaction_percentages = satisfaction_counts / satisfaction_counts.sum() * 100

    # Determine slices to explode: explode if less than 5%
    explode = (satisfaction_percentages < 5).astype(float) * 0.1  # Explode by 0.1 if less than 5%

    # Create a pie chart
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(satisfaction_counts, labels=satisfaction_counts.index, autopct='%1.1f%%',
                                      startangle=90, colors=plt.cm.Pastel1.colors, explode=explode, pctdistance=0.85)
    # ax.set_title('Overall Satisfaction with Logitech Products')

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')


    plt.tight_layout()  # Adjust layout to make room for labels
    plt.show()

def satisfaction_pie_absolute():

    satisfaction_columns = [col for col in data.columns if col.startswith('How satisfied are you with your')]

    # Calculate the average satisfaction score for each respondent if they have rated at least one product
    data['Overall Satisfaction'] = data[satisfaction_columns].mean(axis=1, skipna=True).round()

    # Map numerical scores to textual labels
    satisfaction_labels = {
        1.0: 'Very Dissatisfied',
        2.0: 'Dissatisfied',
        3.0: 'Neutral',
        4.0: 'Satisfied',
        5.0: 'Very Satisfied'
    }
    data['Overall Satisfaction Label'] = data['Overall Satisfaction'].map(satisfaction_labels)

    # Count the occurrences of each satisfaction level
    satisfaction_counts = data['Overall Satisfaction Label'].value_counts()

    # Calculate the percentage for each slice to determine explosion
    satisfaction_percentages = satisfaction_counts / satisfaction_counts.sum() * 100

    # Determine slices to explode: explode if less than 5%
    explode = (satisfaction_percentages < 5).astype(float) * 0.1  # Explode by 0.1 if less than 5%

    # Create a pie chart
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(satisfaction_counts, labels=satisfaction_counts.index,
                                      autopct=lambda p: f'{int(p / 100 * sum(satisfaction_counts))}',
                                      startangle=90, colors=plt.cm.Pastel1.colors, explode=explode,
                                      pctdistance=0.85)
    ax.set_title('Overall Satisfaction with Logitech Products')

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')

    plt.tight_layout()  # Adjust layout to make room for labels
    plt.show()

def plot_satisfaction_distribution():
    # Filter columns related to satisfaction
    satisfaction_columns = [col for col in data.columns if col.startswith('How satisfied are you with your')]

    # Calculate the average satisfaction score for each respondent if they have rated at least one product
    data['Overall Satisfaction'] = data[satisfaction_columns].mean(axis=1, skipna=True).round()

    # Count the occurrences of each satisfaction level
    score_counts = data['Overall Satisfaction'].value_counts(normalize=True).sort_index() * 100

    # Calculate mean, standard deviation, and confidence interval
    mean_satisfaction = data['Overall Satisfaction'].mean()
    std_deviation = data['Overall Satisfaction'].std()
    ci_low, ci_high = norm.interval(confidence=0.95, loc=mean_satisfaction, scale=std_deviation / np.sqrt(len(data)))

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(score_counts.index, score_counts, color='skyblue', label=f'Standard Deviation={std_deviation:.2f}')

    # Mark the average satisfaction and confidence intervals
    ax.axvline(x=mean_satisfaction, color='red', linestyle='--', linewidth=2,
               label=f'Mean Satisfaction={mean_satisfaction:.2f}')
    ax.axvline(x=ci_low, color='green', linestyle='--', linewidth=2, label=f'95% CI Lower={ci_low:.2f}')
    ax.axvline(x=ci_high, color='green', linestyle='--', linewidth=2, label=f'95% CI Upper={ci_high:.2f}')

    # Add labels above each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.1f}%', ha='center', va='bottom')

    # Formatting
    ax.set_xlabel('Satisfaction Score')
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Distribution of Overall Satisfaction Scores')
    ax.legend()

    plt.xticks(np.arange(1, 6))  # Display only numeric scores on the x-axis
    plt.show()

def plot_satisfaction_distribution_fractional(data_fractional):
    # Calculate the total count of responses
    total_count = data_fractional['Count'].sum()

    # Calculate mean, standard deviation, and confidence interval
    mean_satisfaction = (data_fractional['Score'] * data_fractional['Count']).sum() / total_count
    variance = ((data_fractional['Score'] - mean_satisfaction) ** 2 * data_fractional['Count']).sum() / (total_count - 1)
    std_deviation = np.sqrt(variance)
    ci_low, ci_high = norm.interval(confidence=0.95, loc=mean_satisfaction, scale=std_deviation / np.sqrt(total_count))

    # Calculate the percentage for each score
    data_fractional['Percentage'] = (data_fractional['Count'] / total_count) * 100

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(data_fractional['Score'], data_fractional['Percentage'], color='skyblue', label=f'Standard Deviation={std_deviation:.2f}')

    # Mark the average satisfaction and confidence intervals
    ax.axvline(x=mean_satisfaction, color='red', linestyle='--', linewidth=2,
               label=f'Mean Satisfaction={mean_satisfaction:.2f}')
    ax.axvline(x=ci_low, color='green', linestyle='--', linewidth=2, label=f'95% CI Lower={ci_low:.2f}')
    ax.axvline(x=ci_high, color='green', linestyle='--', linewidth=2, label=f'95% CI Upper={ci_high:.2f}')

    # Add labels above each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.1f}%', ha='center', va='bottom')

    # Formatting
    ax.set_xlabel('Satisfaction Score')
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Overall Satisfaction with 100 responses (narrowing of CI)')
    ax.legend()

    plt.xticks(np.arange(1, 6))  # Display only numeric scores on the x-axis
    plt.show()

if __name__ == '__main__':
    data_fractional_adjusted = pd.DataFrame({
        'Score': [5, 4, 3, 1],
        'Count': [63, 22.2, 11.1, 3.7]
    })
    # satisfaction_pie()
    satisfaction_pie_absolute()
    # plot_satisfaction_distribution()
    # plot_satisfaction_distribution_fractional(data_fractional_adjusted)
