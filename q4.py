import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint

data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech.csv")


def usage_duration_percentual_pie():
    usage_counts = data['How long have you been a user or owner of a Logitech product?'].value_counts()
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        usage_counts,
        labels=None,
        autopct=lambda p: '{:.0f}'.format(p * sum(usage_counts) / 100),
        startangle=90,
        colors=plt.cm.Pastel1.colors,
        pctdistance=0.85,
    )

    ax.legend(wedges, usage_counts.index, title="Usage Duration", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    ax.set_title('Duration of Using Logitech Products (Absolute Numbers)')

    ax.axis('equal')

    plt.tight_layout()
    plt.show()


def usage_duration_percent_pie():
    usage_counts = data['How long have you been a user or owner of a Logitech product?'].value_counts()

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        usage_counts,
        labels=None,
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Pastel1.colors,
        pctdistance=0.85,
        explode=[0.1 if pct < 5 else 0 for pct in usage_counts/usage_counts.sum()*100]  # Explode small slices
    )

    ax.legend(wedges, usage_counts.index, title="Usage Duration", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    ax.set_title('Duration of using Logitech products')

    ax.axis('equal')

    plt.tight_layout()
    plt.show()


def bar_absolute_pareto():
    usage_counts = data['How long have you been a user or owner of a Logitech product?'].value_counts().sort_values(
        ascending=False)
    percentages = usage_counts / usage_counts.sum() * 100

    cumulative_percentage = np.cumsum(percentages)

    fig, ax = plt.subplots()
    ax.bar(percentages.index, percentages, color='skyblue')

    ax.plot(percentages.index, cumulative_percentage, color='deeppink', marker='o', linestyle='-', linewidth=2,
            markersize=5)

    ax.set_xlabel('Usage Duration')
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Usage Duration of Logitech Products with Pareto Chart (Percentages)')
    plt.show()


def conf_intervals():
    grouped = data['How long have you been a user or owner of a Logitech product?'].value_counts()
    total_responses = grouped.sum()
    proportions = grouped / total_responses
    conf_ints = {label: proportion_confint(grouped[label], total_responses, alpha=0.05, method='wilson')
                 for label in grouped.index}

    labels = grouped.index
    values = [proportions[label] * 100 for label in labels]
    conf_lower = [conf_ints[label][0] * 100 for label in labels]
    conf_upper = [conf_ints[label][1] * 100 for label in labels]
    errors = [(values[i] - conf_lower[i], conf_upper[i] - values[i]) for i in range(len(values))]

    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(labels, values, yerr=np.array(errors).T, color='skyblue', capsize=5)
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Duration of Using Logitech Products with Confidence Intervals')
    ax.set_ylim(0, 100)

    ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())

    for bar, lower, upper in zip(bars, conf_lower, conf_upper):
        ax.text(bar.get_x() + bar.get_width() / 2, upper + 1, f'{upper:.1f}%', ha='center', va='bottom')
        if lower < 5:
            ax.text(bar.get_x() + bar.get_width() / 2 + 0.05, lower - 0.5, f'{lower:.1f}%', ha='left', va='bottom')
        else:
            ax.text(bar.get_x() + bar.get_width() / 2, lower - 1, f'{lower:.1f}%', ha='center', va='top')

    plt.tight_layout()
    plt.show()


def plot_age_vs_usage_duration():
    age_categories = ["16-20", "21-30", "41-55", "55+"]

    grouped = data.groupby(
        ['How old are you?', 'How long have you been a user or owner of a Logitech product?']).size().unstack(
        fill_value=0)

    grouped = grouped.reindex(age_categories)

    grouped_percent = grouped.div(grouped.sum(axis=1), axis=0) * 100

    ordered_columns = grouped.sum().sort_values(ascending=False).index
    grouped_percent = grouped_percent[ordered_columns]

    # Create a stacked bar chart
    ax = grouped_percent.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Percentage of Users (%)')
    ax.set_title('Usage Duration by Age Group as Percentages')
    ax.legend(title='Usage Duration', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    usage_duration_percent_pie()
    bar_absolute_pareto()
    conf_intervals()
    plot_age_vs_usage_duration()
