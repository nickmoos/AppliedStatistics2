import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

from statsmodels.stats.proportion import proportion_confint

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


def create_pie():
    # Load the data using StringIO to handle the string as file-like object
    data = pd.read_csv(StringIO(csv_data))

    # Count the number of users who use and do not use Logitech products
    use_counts = data['Do you use any Logitech products?'].value_counts()

    # Plotting the data
    fig, ax = plt.subplots()
    ax.pie(use_counts, labels=use_counts.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'tomato'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title('Proportion of Users Who Use/Do Not Use Logitech Products')
    plt.show()

def create_confidence():
    # Load the data using StringIO to handle the string as file-like object
    data = pd.read_csv(StringIO(csv_data))

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
    data = pd.read_csv(StringIO(csv_data))
    # Filter out rows where the response to Logitech product use is missing
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
    data = pd.read_csv(StringIO(csv_data))
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