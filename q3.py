import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint

data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech.csv")

def create_pie_percentual():

    # Assuming the column name is exactly 'Were you aware that the product was made by Logitech when you purchased it?'
    # Check your actual column names and adjust if necessary
    awareness_counts = data['Were you aware that the product was made by Logitech when you purchased it?'].value_counts()

    # Plotting the data
    fig, ax = plt.subplots()
    ax.pie(awareness_counts, labels=awareness_counts.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'tomato'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title('Awareness of Logitech Brand at Purchase')
    plt.show()

def awareness_by_age():
    # Clean column names to ensure they can be accessed easily
    data.columns = [col.replace('\n', ' ').strip() for col in data.columns]

    # Group data by age and awareness
    grouped = data.groupby('How old are you?')[
        'Were you aware that the product was made by Logitech when you purchased it?'].value_counts(
        normalize=True).unstack(fill_value=0)

    # We're interested in the proportion of 'Yes' responses
    awareness_proportions = grouped['Yes'] * 100  # Convert to percentage

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(awareness_proportions.index, awareness_proportions, color='skyblue')
    plt.xlabel('Age Category')
    plt.ylabel('Percentage Aware (%)')
    plt.title('Awareness of Logitech Brand at Purchase by Age Group')

    # Adding percentage format to the y-axis
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())

    # Annotating the bars with the percentage value
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.1f}%', ha='center', va='bottom')

    plt.show()


def awareness_by_age_absolute():
    data.columns = [col.replace('\n', ' ').strip() for col in data.columns]

    # Group data by age and awareness
    grouped = data.groupby('How old are you?')[
        'Were you aware that the product was made by Logitech when you purchased it?'].value_counts().unstack(
        fill_value=0)

    # Extract counts for 'Yes' and 'No' responses
    yes_counts = grouped.get('Yes', pd.Series())
    no_counts = grouped.get('No', pd.Series())

    # Create the bar chart with stacked bars for 'Not Aware'
    plt.figure(figsize=(10, 6))
    bars_yes = plt.bar(yes_counts.index, yes_counts, color='skyblue', label='Aware')
    bars_no = plt.bar(no_counts.index, no_counts, bottom=yes_counts, color='tomato', label='Not Aware')

    plt.xlabel('Age Category')
    plt.ylabel('Number of Responses')
    plt.title('Awareness of Logitech Brand at Purchase by Age Group')

    # Annotating the bars with the absolute number
    for bar, yval in zip(bars_yes, yes_counts):
        plt.text(bar.get_x() + bar.get_width() / 2, yval / 2, f'{int(yval)}', ha='center', va='center')

    for bar, nval, yval in zip(bars_no, no_counts, yes_counts):
        if nval > 0:  # Only display label for 'Not Aware' if there are such responses
            total_height = yval + nval
            plt.text(bar.get_x() + bar.get_width() / 2, yval + nval / 2, f'{int(nval)}', ha='center', va='center')

    plt.legend()
    plt.show()

def create_awareness_with_confidence_intervals():
    # Calculate proportions and confidence intervals
    grouped = data['Were you aware that the product was made by Logitech when you purchased it?'].value_counts()
    total_responses = grouped.sum()
    proportions = grouped / total_responses
    conf_ints = {response: proportion_confint(grouped[response], total_responses, alpha=0.05, method='wilson')
                 for response in grouped.index}

    # Prepare data for plotting
    labels = ['Yes', 'No']
    values = [proportions.get(label, 0) * 100 for label in labels]
    conf_lower = [conf_ints[label][0] * 100 for label in labels]
    conf_upper = [conf_ints[label][1] * 100 for label in labels]
    errors = [(values[i] - conf_lower[i], conf_upper[i] - values[i]) for i in range(len(values))]

    # Create the bar chart with error bars
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(labels, values, yerr=np.array(errors).T, color=['skyblue', 'tomato'], capsize=5)
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Awareness of Logitech Brand at Purchase 95% confidence interval')
    ax.set_ylim(0,100)

    # Adding percentage format to the y-axis
    ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())

    # Annotate bars with the exact bounds
    for bar, lower, upper in zip(bars, conf_lower, conf_upper):
        ax.text(bar.get_x() + bar.get_width() / 2, upper + 1, f'{upper:.1f}%', ha='center', va='bottom', color='black')
        ax.text(bar.get_x() + bar.get_width() / 2, lower - 1, f'{lower:.1f}%', ha='center', va='top', color='black')

    plt.tight_layout()  # Adjust layout to make room for label placement
    plt.show()


def create_awareness_with_variable_samples(total_responses):
    # Exact response counts
    yes_count = int(round(0.857 * total_responses))
    no_count = total_responses - yes_count

    # Generating the data
    data = pd.DataFrame({
        'Were you aware that the product was made by Logitech when you purchased it?':
            ['Yes'] * yes_count + ['No'] * no_count
    })

    # Calculating proportions and confidence intervals
    grouped = data['Were you aware that the product was made by Logitech when you purchased it?'].value_counts()
    proportions = grouped / total_responses
    conf_ints = {response: proportion_confint(grouped[response], total_responses, alpha=0.05, method='wilson')
                 for response in grouped.index}

    # Preparing data for plotting
    labels = ['Yes', 'No']
    values = [proportions[label] * 100 for label in labels]  # Convert proportions to percentages
    conf_lower = [conf_ints[label][0] * 100 for label in labels]
    conf_upper = [conf_ints[label][1] * 100 for label in labels]
    errors = [[(value - lower), (upper - value)] for value, lower, upper in zip(values, conf_lower, conf_upper)]

    # Create the bar chart with error bars
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(labels, values, yerr=np.transpose(errors), color=['skyblue', 'tomato'], capsize=5)
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Awareness of Logitech Brand confidence interval (100 responses)')
    ax.set_ylim(0, 100)

    # Adding percentage format to the y-axis
    ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())

    # Annotate bars with exact bounds
    for bar, lower, upper in zip(bars, conf_lower, conf_upper):
        ax.text(bar.get_x() + bar.get_width() / 2, upper + 1, f'{upper:.1f}%', ha='center', va='bottom', color='black')
        ax.text(bar.get_x() + bar.get_width() / 2, lower - 1, f'{lower:.1f}%', ha='center', va='top', color='black')

    plt.tight_layout()  # Adjust layout to make room for label placement
    plt.show()


if __name__ == '__main__':
    # create_pie_percentual()
    # awareness_by_age()
    # awareness_by_age_absolute()
    # create_awareness_with_confidence_intervals()
    create_awareness_with_variable_samples(100)