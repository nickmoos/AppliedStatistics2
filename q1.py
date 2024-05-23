import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint
from io import StringIO

data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech.csv")

def create_proportional_conf_intervals():

    # List of all potential age categories
    age_categories = ["16-20", "21-30", "31-40", "41-55", "55+"]

    # Initialize lists to store the results
    lower_bounds = []
    upper_bounds = []
    categories_with_data = []

    # Calculate confidence intervals for each age category
    for category in age_categories:
        count = sum(data['How old are you?'] == category)
        nobs = len(data['How old are you?'])  # total number of observations

        if count > 0:
            confint = proportion_confint(count, nobs, alpha=0.05, method='wilson')
            lower_bounds.append(confint[0] * 100)  # Convert to percentage
            upper_bounds.append(confint[1] * 100)  # Convert to percentage
            categories_with_data.append(category)

    # Errors for the error bars (as percentage)
    errors = [(upper - lower) / 2 for lower, upper in zip(lower_bounds, upper_bounds)]

    # Center of the error bars (as percentage)
    means = [(lower + upper) / 2 for lower, upper in zip(lower_bounds, upper_bounds)]

    # Create the plot
    plt.figure(figsize=(10, 5))
    bars = plt.bar(categories_with_data, means, yerr=errors, capsize=5, color='skyblue')
    plt.xlabel('Age Category')
    plt.ylabel('Proportion (%)')
    plt.title('95% Confidence Intervals for Proportion of Age Categories')

    # Adding percentage format to the y-axis
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())

    # Annotating the bars with the exact percentage values for bounds
    for bar, lower, upper in zip(bars, lower_bounds, upper_bounds):
        plt.text(bar.get_x() + bar.get_width() / 2 + 0.3, lower + 1, f'{lower:.1f}%', ha='right',
                 va='top')  # Adjusted position
        plt.text(bar.get_x() + bar.get_width() / 2, upper + 0.5, f'{upper:.1f}%', ha='center',
                 va='bottom')  # Slightly raised upper bound text

    plt.show()

def create_simple_percentage_plot():

    # List of all potential age categories
    age_categories = ["16-20", "21-30", "41-55", "55+"]

    # Initialize list to store the results
    percentages = []

    # Calculate percentage for each age category
    total_count = len(data['How old are you?'])  # total number of observations
    for category in age_categories:
        count = sum(data['How old are you?'] == category)
        if count > 0:
            category_percentage = (count / total_count) * 100
        else:
            category_percentage = 0  # To handle categories with no data
        percentages.append(category_percentage)

    # Create the plot
    plt.figure(figsize=(10, 5))
    bars = plt.bar(age_categories, percentages, color='skyblue')
    plt.xlabel('Age Category')
    plt.ylabel('Proportion (%)')
    plt.title('Proportion of Age Categories')

    # Adding percentage format to the y-axis
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())

    # Annotating the bars with the percentage value
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.1f}%', ha='center', va='bottom')

    plt.show()

def create_pareto_chart():

    # List of all potential age categories
    age_categories = ["16-20", "21-30", "41-55", "55+"]

    # Initialize lists to store the results
    counts = []
    categories_with_data = []

    # Calculate the count for each age category
    total_count = len(data['How old are you?'])  # total number of observations
    for category in age_categories:
        count = sum(data['How old are you?'] == category)
        if count > 0:
            counts.append(count)
            categories_with_data.append(category)

    # Sort categories by count in descending order for Pareto chart
    categories_with_counts = sorted(zip(categories_with_data, counts), key=lambda x: x[1], reverse=True)
    sorted_categories, sorted_counts = zip(*categories_with_counts)

    # Calculate cumulative percentages
    cumulative_percentages = np.cumsum(sorted_counts) / total_count * 100

    # Create the plot with bars and a line for the cumulative percentages
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Bars for the individual counts
    bars = ax1.bar(sorted_categories, sorted_counts, color='skyblue', label='Count')
    ax1.set_xlabel('Age Category')
    ax1.set_ylabel('Count')
    ax1.set_title('Pareto Chart of Age Category Counts and Cumulative Percentages')

    # Line plot for the cumulative percentages
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.plot(sorted_categories, cumulative_percentages, color='red', marker='o', label='Cumulative Percentage')
    ax2.set_ylabel('Cumulative Proportion (%)')

    # Adding percentage format to the cumulative y-axis
    ax2.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())

    # Annotating the bars with the count value
    for bar, value in zip(bars, sorted_counts):
        ax1.text(bar.get_x() + bar.get_width() / 2, value, f'{int(value)}', ha='center', va='bottom')

    fig.tight_layout()  # to ensure the right y-label is not slightly clipped
    plt.show()

if __name__ == '__main__':
    create_proportional_conf_intervals()
    # create_simple_percentage_plot()
    # create_pareto_chart()