import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

from statsmodels.stats.proportion import proportion_confint

data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech.csv")

def create_pie():

    # Count the number of users who use and do not use Logitech products
    use_counts = data['Do you use any Logitech products?'].value_counts()

    # Plotting the data
    fig, ax = plt.subplots()
    ax.pie(use_counts, labels=use_counts.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'tomato'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title('Proportion of Users Who Use/Do Not Use Logitech Products')
    plt.show()

def create_confidence():
    # Count the number of users who use and do not use Logitech products
    use_counts = data['Do you use any Logitech products?'].value_counts()

    # Total observations
    total_responses = use_counts.sum()

    # Convert counts to percentages
    percentages = use_counts / total_responses * 100

    # Calculate confidence intervals for proportions
    conf_intervals = {}
    for response in use_counts.index:
        count = use_counts[response]
        conf_interval = proportion_confint(count, total_responses, alpha=0.05, method='wilson')
        conf_intervals[response] = conf_interval

    # Convert confidence intervals to percentages
    conf_percentages = {key: (val[0] * 100, val[1] * 100) for key, val in conf_intervals.items()}

    # Plotting the bar chart with error bars
    fig, ax = plt.subplots()
    bars = ax.bar(percentages.index, percentages, color=['skyblue', 'tomato'], yerr=[
        (percentages[key] - conf_percentages[key][0], conf_percentages[key][1] - percentages[key]) for key in
        percentages.index
    ], capsize=5)

    # Adding text annotations for the center points of the confidence intervals
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.1f}%', ha='center', va='bottom')

    ax.set_ylabel('Percentage')
    ax.set_title('95% Confidence Intervals for Proportion of Users Who Use/\nDo Not Use Logitech Products')
    ax.set_ylim(0, 100)  # Adjust as necessary to fit annotations

    plt.show()

def age_groups_that_use_logitech_chart():
    data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech.csv")
    data = data[data['Do you use any Logitech products?'].notna()]

    # Group by age and Logitech product usage
    grouped = data.groupby('How old are you?')['Do you use any Logitech products?'].value_counts(
        normalize=True).unstack(fill_value=0)

    # We are interested in the proportion of 'Yes' responses
    proportions = grouped['Yes'] * 100  # Convert to percentage

    # Optionally, calculate confidence intervals for these proportions
    nobs = data.groupby('How old are you?').size()
    conf_ints = {age: proportion_confint(nobs[age] * proportions[age] / 100, nobs[age], alpha=0.05, method='wilson')
                 for age in proportions.index}

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(proportions.index, proportions, color='skyblue', capsize=5)
    plt.xlabel('Age Category')
    plt.ylabel('Percentage Using Logitech Products (%)')
    plt.title('Usage of Logitech Products by Age Category')

    # Adding percentage format to the y-axis
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())

    # Annotate each bar with the percentage value
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.1f}%', ha='center', va='bottom')

    plt.show()

def age_groups_that_use_logitech_chart_absolute_numbers():
    data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech.csv")
    # Filter out rows where the response to Logitech product use is missing
    data = data[data['Do you use any Logitech products?'].notna()]

    # Group by age and Logitech product usage
    grouped = data.groupby('How old are you?')['Do you use any Logitech products?'].value_counts().unstack(fill_value=0)

    # Counts of 'Yes' and 'No' responses
    yes_counts = grouped['Yes']
    no_counts = grouped['No']

    # Create the bar chart with stacked bars
    plt.figure(figsize=(10, 6))
    bars_yes = plt.bar(yes_counts.index, yes_counts, color='skyblue', label='Yes', capsize=5)
    bars_no = plt.bar(no_counts.index, no_counts, bottom=yes_counts, color='tomato', label='No', capsize=5)

    plt.xlabel('Age Category')
    plt.ylabel('Number of Users')
    plt.title('Number of Users Using Logitech Products by Age Category')

    # Annotate each bar with the exact count
    for bar, yval in zip(bars_yes, yes_counts):
        plt.text(bar.get_x() + bar.get_width() / 2, yval / 2, f'{int(yval)}', ha='center', va='center')

    for bar, nval, yval in zip(bars_no, no_counts, yes_counts):
        if nval > 0:
            total_height = yval + nval  # Total height of stacked bar
            plt.text(bar.get_x() + bar.get_width() / 2, yval + (nval / 2), f'{int(nval)}', ha='center', va='center')

    plt.legend()
    plt.show()

if __name__ == '__main__':
    # create_pie()
    create_confidence()
    # age_groups_that_use_logitech_chart()
    # age_groups_that_use_logitech_chart_absolute_numbers()