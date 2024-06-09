import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint

data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech.csv")


def create_proportional_conf_intervals():
    age_categories = ["16-20", "21-30", "31-40", "41-55", "55+"]

    lower_bounds = []
    upper_bounds = []
    categories_with_data = []

    for category in age_categories:
        count = sum(data['How old are you?'] == category)
        nobs = len(data['How old are you?'])

        if count > 0:
            confint = proportion_confint(count, nobs, alpha=0.05, method='wilson')
            lower_bounds.append(confint[0] * 100)
            upper_bounds.append(confint[1] * 100)
            categories_with_data.append(category)

    errors = [(upper - lower) / 2 for lower, upper in zip(lower_bounds, upper_bounds)]

    means = [(lower + upper) / 2 for lower, upper in zip(lower_bounds, upper_bounds)]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(categories_with_data, means, yerr=errors, capsize=5, color='skyblue')
    plt.xlabel('Age Category')
    plt.ylabel('Proportion (%)')
    plt.title('95% Confidence Intervals for Proportion of Age Categories')

    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())

    for bar, lower, upper in zip(bars, lower_bounds, upper_bounds):
        plt.text(bar.get_x() + bar.get_width() / 2 + 0.3, lower + 1, f'{lower:.1f}%', ha='right',
                 va='top')
        plt.text(bar.get_x() + bar.get_width() / 2, upper + 0.5, f'{upper:.1f}%', ha='center',
                 va='bottom')

    plt.show()


def create_simple_percentage_plot():
    age_categories = ["16-20", "21-30", "41-55", "55+"]

    percentages = []

    total_count = len(data['How old are you?'])
    for category in age_categories:
        count = sum(data['How old are you?'] == category)
        if count > 0:
            category_percentage = (count / total_count) * 100
        else:
            category_percentage = 0
        percentages.append(category_percentage)

    plt.figure(figsize=(10, 5))
    bars = plt.bar(age_categories, percentages, color='skyblue')
    plt.xlabel('Age Category')
    plt.ylabel('Proportion (%)')
    plt.title('Proportion of Age Categories')

    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.1f}%', ha='center', va='bottom')

    plt.show()


def create_simple_bar_chart():
    age_categories = ["16-20", "21-30", "41-55", "55+"]

    percentages = []

    total_count = len(data['How old are you?'])
    for category in age_categories:
        count = sum(data['How old are you?'] == category)
        if count > 0:
            category_percentage = (count / total_count) * 100
        else:
            category_percentage = 0
        percentages.append(category_percentage)

    fig, ax = plt.subplots()
    ax.pie(percentages, labels=age_categories, autopct='%1.1f%%',
                                      startangle=90, colors=plt.cm.Pastel1.colors)
    ax.set_title('Proportion of Age Categories')

    ax.axis('equal')

    plt.tight_layout()
    plt.show()


def create_pareto_chart():
    age_categories = ["16-20", "21-30", "41-55", "55+"]

    counts = []
    categories_with_data = []

    total_count = len(data['How old are you?'])
    for category in age_categories:
        count = sum(data['How old are you?'] == category)
        if count > 0:
            counts.append(count)
            categories_with_data.append(category)

    categories_with_counts = sorted(zip(categories_with_data, counts), key=lambda x: x[1], reverse=True)
    sorted_categories, sorted_counts = zip(*categories_with_counts)

    cumulative_percentages = np.cumsum(sorted_counts) / total_count * 100

    fig, ax1 = plt.subplots(figsize=(10, 5))

    bars = ax1.bar(sorted_categories, sorted_counts, color='skyblue', label='Count')
    ax1.set_xlabel('Age Category')
    ax1.set_ylabel('Count')
    ax1.set_title('Age Categories')

    ax2 = ax1.twinx()
    ax2.plot(sorted_categories, cumulative_percentages, color='red', marker='o', label='Cumulative Percentage')
    ax2.set_ylabel('Cumulative Proportion (%)')

    ax2.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())

    for bar, value in zip(bars, sorted_counts):
        ax1.text(bar.get_x() + bar.get_width() / 2, value, f'{int(value)}', ha='center', va='bottom')

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    create_proportional_conf_intervals()
    create_simple_percentage_plot()
    create_pareto_chart()
    create_simple_bar_chart()
