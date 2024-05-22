import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint
from io import StringIO

csv_data = """
Timestamp,How old are you?,Do you use any Logitech products?,"Were you aware that the product was
made by Logitech when you purchased it?",How long have you been a user or owner of a Logitech product?,What Logitech Product do you use the most?,How satisfied are you with your Logitech mouse?,What qualities are you satisfied with? ,What qualities are you dissatisfied with? ,How satisfied are you with your Logitech keyboard?,What qualities are you satisfied with? .1,What qualities are you dissatisfied with? .1,How satisfied are you with your Logitech webcam?,What qualities are you satisfied with? .2,What qualities are you dissatisfied with? .2,How satisfied are you with your Logitech headset?,What qualities are you satisfied with? .3,What qualities are you dissatisfied with? .3,How satisfied are you with your Logitech speakers?,What qualities are you satisfied with? .4,What qualities are you dissatisfied with? .4,How satisfied are you with your Logitech product?,What qualities are you satisfied with? .5,What qualities are you dissatisfied with? .5,If you ever had an issue with your logitech product whom did you contact your retailer or logitech customer service? ,Were you satisfied with Logitech customer service?,How likely are you to recommend Logitech products to others?
2024/03/04 3:18:36 pm EET,21-30,Yes,Yes,More than 3 years,Mouse,5,Durability,,,,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/03/04 3:28:40 pm EET,16-20,Yes,Yes,More than 3 years,Webcam,,,,,,,4,Ease of use;Durability,Features,,,,,,,,,,I never had an issue with my product,,Likely
2024/03/04 3:29:31 pm EET,21-30,Yes,Yes,More than 3 years,Mouse and Keyboard. It is not possible to choose multiple options. Fix this Nick,,,,,,,,,,,,,,,,3,Ease of use;Value for money,Features,I never had an issue with my product,,Unlikely
2024/03/04 4:55:14 pm EET,16-20,No,,,,,,,,,,,,,,,,,,,,,,,,
2024/03/04 4:58:54 pm EET,21-30,Yes,No,More than 3 years,Mouse,3,Ease of use;Durability,Value for money;Performance,,,,,,,,,,,,,,,,I never had an issue with my product,,It depends
2024/03/04 6:28:19 pm EET,55+,Yes,Yes,More than 3 years,Mouse,5,Ease of use;Value for money;Durability;Performance,,,,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/03/04 8:59:00 pm EET,21-30,Yes,Yes,Less than 6 months,Mouse,5,Features;Performance,,,,,,,,,,,,,,,,,I never had an issue with my product,,It depends
2024/03/05 3:27:40 am EET,21-30,Yes,Yes,More than 3 years,Game controller,,,,,,,,,,,,,,,,5,Durability;Performance,Value for money,I never had an issue with my product,,Likely
2024/03/05 1:00:44 pm EET,21-30,Yes,Yes,More than 3 years,Joystick / Controller ,,,,,,,,,,,,,,,,5,Value for money;Features;Performance,,I never had an issue with my product,,It depends
2024/03/10 3:44:53 pm EET,16-20,Yes,Yes,6 months to a year,Mouse,5,Ease of use;Durability;Performance,Value for money,,,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/03/10 3:47:31 pm EET,16-20,No,,,,,,,,,,,,,,,,,,,,,,,,
2024/03/10 3:51:53 pm EET,16-20,Yes,No,1-3 years,Mousepad,,,,,,,,,,,,,,,,4,Durability;Performance,Value for money,I never had an issue with my product,,Likely
2024/03/10 3:59:36 pm EET,16-20,No,,,,,,,,,,,,,,,,,,,,,,,,
2024/03/10 6:18:40 pm EET,16-20,Yes,Yes,1-3 years,Mouse,5,Performance,Value for money,,,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/03/10 6:19:50 pm EET,16-20,Yes,No,1-3 years,Mouse,4,Ease of use;Performance,,,,,,,,,,,,,,,,,I never had an issue with my product,,It depends
2024/03/10 6:22:22 pm EET,55+,Yes,Yes,More than 3 years,Mouse,1,Ease of use;Performance,Value for money;Durability,,,,,,,,,,,,,,,,Retailer,,Unlikely
2024/03/10 6:29:14 pm EET,16-20,Yes,Yes,1-3 years,Mouse,5,Durability;Performance,Value for money,,,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/03/10 6:40:25 pm EET,16-20,Yes,Yes,1-3 years,Mouse,4,Performance,,,,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/03/11 10:20:42 pm EET,41-55,Yes,Yes,More than 3 years,Mouse,5,Ease of use;Value for money;Durability;Performance,,,,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/04/08 2:34:09 pm EET,16-20,Yes,Yes,1-3 years,Mouse,5,Ease of use;Durability;Performance,Features,,,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/04/09 10:24:46 am EET,41-55,Yes,Yes,More than 3 years,Mouse,3,Ease of use;Value for money,Ease of use;Value for money;Features;Durability;Performance,,,,,,,,,,,,,,,,I never had an issue with my product,,It depends
2024/04/15 12:33:29 pm EET,16-20,No,,,,,,,,,,,,,,,,,,,,,,,,
2024/04/15 12:37:05 pm EET,21-30,Yes,Yes,More than 3 years,Mouse,5,Ease of use;Durability;Performance,,,,,,,,,,,,,,,,,I never had an issue with my product,,It depends
2024/04/15 12:37:44 pm EET,21-30,Yes,No,More than 3 years,Headset,,,,,,,,,,4,Ease of use;Durability,,,,,,,,I never had an issue with my product,,It depends
2024/04/15 12:42:33 pm EET,21-30,Yes,Yes,6 months to a year,Mouse,5,Ease of use;Durability;Performance,,,,,,,,,,,,,,,,,I never had an issue with my product,,It depends
2024/04/15 12:51:12 pm EET,16-20,Yes,Yes,1-3 years,Mouse,5,Ease of use;Value for money;Features;Durability;Performance,,,,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/04/15 12:54:17 pm EET,21-30,Yes,Yes,More than 3 years,bro I have a mouse as well as a tastatur and mostly use them the sime time,,,,,,,,,,,,,,,,5,Ease of use;Features;Durability;Performance,Value for money,Retailer,,Likely
2024/04/15 12:56:08 pm EET,16-20,Yes,Yes,More than 3 years,Mouse,5,Ease of use;Durability;Performance,,,,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/04/15 2:00:58 pm EET,16-20,No,,,,,,,,,,,,,,,,,,,,,,,,
2024/04/15 2:31:33 pm EET,21-30,Yes,Yes,1-3 years,Mouse,4,Ease of use;Value for money;Durability,Features,,,,,,,,,,,,,,,,I never had an issue with my product,,It depends
2024/04/15 4:44:46 pm EET,21-30,Yes,Yes,More than 3 years,Mouse,5,Ease of use;Features;Performance,,,,,,,,,,,,,,,,,Customer service,Yes,Likely
2024/04/15 6:44:24 pm EET,21-30,Yes,Yes,1-3 years,Keyboard,,,,5,Ease of use;Performance,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/05/06 1:57:48 pm EEST,16-20,Yes,Yes,More than 3 years,Webcam,,,,,,,5,Ease of use;Value for money;Durability;Performance,Features,,,,,,,,,,Retailer,,Likely"""

def create_proportional_conf_intervals():
    # Load the data using StringIO to handle the string as file-like object
    data = pd.read_csv(StringIO(csv_data))

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
    # Load the data using StringIO to handle the string as file-like object
    data = pd.read_csv(StringIO(csv_data))

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
    # Load the data using StringIO to handle the string as file-like object
    data = pd.read_csv(StringIO(csv_data))

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
    # create_proportional_conf_intervals()
    # create_simple_percentage_plot()
    create_pareto_chart()