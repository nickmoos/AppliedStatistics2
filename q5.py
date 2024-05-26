import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint

data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech_Copy.csv")


def pie_chart_absolute():
    product_counts = data['What Logitech Product do you use the most?'].value_counts()

    # Calculate the percentage for each product
    product_percentages = product_counts / product_counts.sum() * 100

    # Determine slices to explode: explode if less than 5%
    explode = (product_percentages < 5).astype(int) * 0.1  # Explode by 0.1 if less than 5%

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(product_counts, labels=product_counts.index, autopct='%1.1f%%', startangle=90,
           colors=plt.cm.Pastel1.colors, explode=explode, pctdistance=0.85)
    ax.set_title('What Logitech products do people use the most')

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')

    plt.tight_layout()  # Adjust layout to make room for labels
    plt.show()

def pie_chart_percents():
    product_counts = data['What Logitech Product do you use the most?'].value_counts()

    # Calculate the percentage for each product to determine explosion
    product_percentages = product_counts / product_counts.sum() * 100

    # Determine slices to explode: explode if less than 5%
    explode = (product_percentages < 5).astype(int) * 0.1  # Explode by 0.1 if less than 5%

    # Create a pie chart with absolute numbers
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(product_counts, labels=product_counts.index,
                                      autopct=lambda p: '{:.0f}'.format(p * sum(product_counts) / 100),
                                      startangle=90, colors=plt.cm.Pastel1.colors, explode=explode,
                                      pctdistance=0.85)
    ax.set_title('Distribution of Most Used Logitech Products (Absolute Numbers)')

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')

    plt.tight_layout()  # Adjust layout to make room for labels
    plt.show()

def bar_chart_pareto():
    product_counts = data['What Logitech Product do you use the most?'].value_counts()

    # Calculate percentages
    total_counts = product_counts.sum()
    product_percentages = product_counts / total_counts * 100

    # Sort data by percentage descending for Pareto
    product_percentages = product_percentages.sort_values(ascending=False)

    # Calculate cumulative percentages for the Pareto line
    cumulative_percentage = product_percentages.cumsum()

    # Create a figure and bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(product_percentages.index, product_percentages, color='skyblue', label='Percentage')

    # Create Pareto line on the same y-axis
    ax.plot(product_percentages.index, cumulative_percentage, color='deeppink', marker='o', linestyle='-', linewidth=2,
            label='Cumulative Percentage')

    # Formatting the plot
    ax.set_xlabel('Product Type')
    ax.set_ylabel('Percentage (%)')
    ax.set_title('What Logitech products do people use the most')
    ax.set_ylim(0, 110)  # Set limits to slightly above 100% for visibility

    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # pie_chart_absolute()
    # pie_chart_percents()
    bar_chart_pareto()