import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech_Copy.csv")


def pie_chart_absolute():
    product_counts = data['What Logitech Product do you use the most?'].value_counts()

    product_percentages = product_counts / product_counts.sum() * 100

    explode = (product_percentages < 5).astype(int) * 0.1

    fig, ax = plt.subplots()
    ax.pie(product_counts, labels=product_counts.index, autopct='%1.1f%%', startangle=90,
           colors=plt.cm.Pastel1.colors, explode=explode, pctdistance=0.85)
    ax.set_title('What Logitech products do people use the most', pad=20)

    ax.axis('equal')

    plt.tight_layout()
    plt.show()


def pie_chart_percents():
    product_counts = data['What Logitech Product do you use the most?'].value_counts()

    product_percentages = product_counts / product_counts.sum() * 100

    explode = (product_percentages < 5).astype(int) * 0.1

    fig, ax = plt.subplots()
    ax.pie(product_counts, labels=product_counts.index,
                                      autopct=lambda p: '{:.0f}'.format(p * sum(product_counts) / 100),
                                      startangle=90, colors=plt.cm.Pastel1.colors, explode=explode,
                                      pctdistance=0.85)
    ax.set_title('Distribution of Most Used Logitech Products (Absolute Numbers)')

    ax.axis('equal')

    plt.tight_layout()
    plt.show()


def bar_chart_pareto():
    product_counts = data['What Logitech Product do you use the most?'].value_counts()

    total_counts = product_counts.sum()
    product_percentages = product_counts / total_counts * 100

    product_percentages = product_percentages.sort_values(ascending=False)

    cumulative_percentage = product_percentages.cumsum()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(product_percentages.index, product_percentages, color='skyblue', label='Percentage')
    ax.plot(product_percentages.index, cumulative_percentage, color='deeppink', marker='o', linestyle='-', linewidth=2,
            label='Cumulative Percentage')

    ax.set_xlabel('Product Type')
    ax.set_ylabel('Percentage (%)')
    ax.set_title('What Logitech products do people use the most')
    ax.set_ylim(0, 110)

    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    pie_chart_absolute()
    pie_chart_percents()
    bar_chart_pareto()
