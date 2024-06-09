import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.stats.proportion import proportion_confint

data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech.csv")


def create_pie():
    use_counts = data['Do you use any Logitech products?'].value_counts()

    fig, ax = plt.subplots()
    ax.pie(use_counts, labels=use_counts.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'tomato'])
    ax.axis('equal')

    plt.title('Proportion of Users Who Use/Do Not Use Logitech Products')
    plt.show()


def create_confidence():
    use_counts = data['Do you use any Logitech products?'].value_counts()

    total_responses = use_counts.sum()
    percentages = use_counts / total_responses * 100

    conf_intervals = {}
    for response in use_counts.index:
        count = use_counts[response]
        conf_interval = proportion_confint(count, total_responses, alpha=0.05, method='wilson')
        conf_intervals[response] = conf_interval

    conf_percentages = {key: (val[0] * 100, val[1] * 100) for key, val in conf_intervals.items()}

    fig, ax = plt.subplots()
    bars = ax.bar(percentages.index, percentages, color=['skyblue', 'tomato'], yerr=[
        (percentages[key] - conf_percentages[key][0], conf_percentages[key][1] - percentages[key]) for key in
        percentages.index
    ], capsize=5)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.1f}%', ha='center', va='bottom')

    ax.set_ylabel('Percentage')
    ax.set_title('95% Confidence Intervals for Proportion of Users Who Use/\nDo Not Use Logitech Products')
    ax.set_ylim(0, 100)

    plt.show()


def age_groups_that_use_logitech_chart():
    data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech.csv")
    data = data[data['Do you use any Logitech products?'].notna()]

    grouped = data.groupby('How old are you?')['Do you use any Logitech products?'].value_counts(
        normalize=True).unstack(fill_value=0)

    proportions = grouped['Yes'] * 100

    nobs = data.groupby('How old are you?').size()
    conf_ints = {age: proportion_confint(nobs[age] * proportions[age] / 100, nobs[age], alpha=0.05, method='wilson')
                 for age in proportions.index}

    plt.figure(figsize=(10, 6))
    bars = plt.bar(proportions.index, proportions, color='skyblue', capsize=5)
    plt.xlabel('Age Category')
    plt.ylabel('Percentage Using Logitech Products (%)')
    plt.title('Usage of Logitech Products by Age Category')

    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.1f}%', ha='center', va='bottom')
    plt.show()


def age_groups_that_use_logitech_chart_absolute_numbers():
    data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech.csv")
    data = data[data['Do you use any Logitech products?'].notna()]

    grouped = data.groupby('How old are you?')['Do you use any Logitech products?'].value_counts().unstack(fill_value=0)

    yes_counts = grouped['Yes']
    no_counts = grouped['No']

    plt.figure(figsize=(10, 6))
    bars_yes = plt.bar(yes_counts.index, yes_counts, color='skyblue', label='Yes', capsize=5)
    bars_no = plt.bar(no_counts.index, no_counts, bottom=yes_counts, color='tomato', label='No', capsize=5)

    plt.xlabel('Age Category')
    plt.ylabel('Number of Users')
    plt.title('Number of Users Using Logitech Products by Age Category')

    for bar, yval in zip(bars_yes, yes_counts):
        plt.text(bar.get_x() + bar.get_width() / 2, yval / 2, f'{int(yval)}', ha='center', va='center')

    for bar, nval, yval in zip(bars_no, no_counts, yes_counts):
        if nval > 0:
            plt.text(bar.get_x() + bar.get_width() / 2, yval + (nval / 2), f'{int(nval)}', ha='center', va='center')

    plt.legend()
    plt.show()


def age_groups_that_use_percentual_yes_no():
    data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech.csv")
    data = data[data['Do you use any Logitech products?'].notna()]

    grouped = data.groupby('How old are you?')['Do you use any Logitech products?'].value_counts(
        normalize=True).unstack(fill_value=0)

    proportions_yes = grouped.get('Yes', 0) * 100
    proportions_no = grouped.get('No', 0) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    bars_yes = ax.bar(proportions_yes.index, proportions_yes, color='skyblue', label='Yes', capsize=5)
    bars_no = ax.bar(proportions_no.index, proportions_no, bottom=proportions_yes, color='tomato', label='No', capsize=5)

    ax.set_xlabel('Age Category')
    ax.set_ylabel('Percentage Using Logitech Products (%)')
    ax.set_title('Usage of Logitech Products by Age Category')

    ax.yaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)

    ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())

    for bar, label in zip(bars_yes, proportions_yes.round(1)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height / 2, f'{label}%', ha='center', va='center', color='white')

    for bar, label in zip(bars_no, proportions_no.round(1)):
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2, f'{label}%', ha='center', va='center', color='white')

    ax.legend(title="Logitech Product Usage")
    plt.show()


if __name__ == '__main__':
    create_pie()
    create_confidence()
    age_groups_that_use_logitech_chart()
    age_groups_that_use_logitech_chart_absolute_numbers()
    age_groups_that_use_percentual_yes_no()
