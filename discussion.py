import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech_Copy.csv")


def satisfaction_vs_recommendation_bar():
    satisfaction_columns = [col for col in data.columns if col.startswith('How satisfied are you with your')]

    data['Overall Satisfaction'] = data[satisfaction_columns].mean(axis=1).round()

    satisfaction_labels = {
        1.0: 'Very Dissatisfied',
        2.0: 'Dissatisfied',
        3.0: 'Neutral',
        4.0: 'Satisfied',
        5.0: 'Very Satisfied'
    }
    data['Overall Satisfaction Label'] = data['Overall Satisfaction'].map(satisfaction_labels)

    recommendation_column = 'How likely are you to recommend Logitech products to others?'
    satisfaction_levels = ['Very Dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very Satisfied']
    recommendation_counts = {level: data[data['Overall Satisfaction Label'] == level][recommendation_column].value_counts(normalize=True) * 100 for level in satisfaction_levels}

    colors = {
        'Likely': 'forestgreen',
        'Unlikely': 'tomato',
        'It depends': 'skyblue'
    }

    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.6
    for i, level in enumerate(satisfaction_levels):
        bottom = 0
        for recommendation in ['Likely', 'Unlikely', 'It depends']:
            count = recommendation_counts[level].get(recommendation, 0)
            ax.bar(level, count, bar_width, bottom=bottom, color=colors[recommendation], label=recommendation if i == 0 else "")
            bottom += count

    for i, level in enumerate(satisfaction_levels):
        bottom = 0
        for recommendation in ['Likely', 'Unlikely', 'It depends']:
            count = recommendation_counts[level].get(recommendation, 0)
            if count > 0:
                ax.text(i, bottom + count / 2, f'{count:.1f}%', ha='center', va='center', color='white', fontweight='bold')
                bottom += count

    ax.set_xlabel('Satisfaction Level')
    ax.yaxis.set_visible(False)
    ax.set_title('Satisfaction Level vs Likelihood to Recommend')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Recommendation')

    plt.tight_layout()
    plt.show()


def dissatisfaction_bar_chart():
    data = {
        'Mouse': {'Ease of use': 1, 'Value for money': 6, 'Features': 3, 'Durability': 2, 'Performance': 2},
        'Keyboard': {'Ease of use': 0, 'Value for money': 1, 'Features': 1, 'Durability': 0, 'Performance': 0},
        'Webcam': {'Ease of use': 0, 'Value for money': 0, 'Features': 2, 'Durability': 0, 'Performance': 0},
        'Controller': {'Ease of use': 0, 'Value for money': 1, 'Features': 0, 'Durability': 0, 'Performance': 0},
        'Mousepad': {'Ease of use': 0, 'Value for money': 1, 'Features': 0, 'Durability': 0, 'Performance': 0}
    }

    categories = list(data.keys())
    causes = ['Ease of use', 'Value for money', 'Features', 'Durability', 'Performance']
    colors = {
        'Ease of use': 'skyblue',
        'Value for money': 'tomato',
        'Features': 'gold',
        'Durability': 'lightgreen',
        'Performance': 'orchid'
    }

    percentages = {}
    for category, causes_data in data.items():
        total_responses = sum(causes_data.values())
        percentages[category] = {cause: (count / total_responses) * 100 for cause, count in causes_data.items()}

    # Prepare the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 0.6

    for i, category in enumerate(categories):
        bottom = 0
        for cause in causes:
            count = percentages[category][cause]
            ax.bar(category, count, bar_width, bottom=bottom, color=colors[cause], label=cause if i == 0 else "")
            bottom += count

    for i, category in enumerate(categories):
        bottom = 0
        for cause in causes:
            count = percentages[category][cause]
            if count > 0:
                ax.text(i, bottom + count / 2, f'{count:.1f}%', ha='center', va='center', color='white', fontweight='bold')
                bottom += count

    ax.set_xlabel('Product Category')
    ax.yaxis.set_visible(False)
    ax.set_title('Causes of Dissatisfaction by Product Category')

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Cause of Dissatisfaction')

    plt.tight_layout()
    plt.show()


def product_awareness_bar_chart():
    product_column = 'What Logitech Product do you use the most?'
    awareness_column = 'Were you aware that the product was made by Logitech when you purchased it?'

    product_categories = data[product_column].unique()
    awareness_counts = {category: data[data[product_column] == category][awareness_column].value_counts() for category in product_categories}

    colors = {
        'Yes': 'forestgreen',
        'No': 'tomato'
    }

    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 0.4
    index = range(len(product_categories))

    for i, category in enumerate(product_categories):
        bottom = 0
        for awareness in ['Yes', 'No']:
            count = awareness_counts[category].get(awareness, 0)
            ax.bar(i, count, bar_width, bottom=bottom, color=colors[awareness], label=awareness if i == 0 else "")
            bottom += count

    for i, category in enumerate(product_categories):
        bottom = 0
        for awareness in ['Yes', 'No']:
            count = awareness_counts[category].get(awareness, 0)
            if count > 0:
                ax.text(i, bottom + count / 2, f'{count}', ha='center', va='center', color='white', fontweight='bold')
                bottom += count

    ax.set_xticks(index)
    ax.set_xticklabels(product_categories)
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Number of Responses')
    ax.set_title('Product Awareness by Product Category')

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Awareness')

    plt.tight_layout()
    plt.show()


def product_awareness_bar_chart_percent():
    product_column = 'What Logitech Product do you use the most?'
    awareness_column = 'Were you aware that the product was made by Logitech when you purchased it?'

    included_categories = ['Mouse', 'Webcam', 'Keyboard', 'Game Controller', 'Mousepad', 'Headset']
    data_filtered = data[data[product_column].isin(included_categories)]

    product_categories = data_filtered[product_column].unique()
    awareness_counts = {category: data_filtered[data_filtered[product_column] == category][awareness_column].value_counts(normalize=True) * 100 for category in product_categories}

    colors = {
        'Yes': 'forestgreen',
        'No': 'tomato'
    }

    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 0.4
    index = range(len(product_categories))

    for i, category in enumerate(product_categories):
        bottom = 0
        for awareness in ['Yes', 'No']:
            count = awareness_counts[category].get(awareness, 0)
            ax.bar(i, count, bar_width, bottom=bottom, color=colors[awareness], label=awareness if i == 0 else "")
            bottom += count

    for i, category in enumerate(product_categories):
        bottom = 0
        for awareness in ['Yes', 'No']:
            count = awareness_counts[category].get(awareness, 0)
            if count > 0:
                ax.text(i, bottom + count / 2, f'{count:.1f}%', ha='center', va='center', color='white', fontweight='bold')
                bottom += count

    ax.set_xticks(index)
    ax.set_xticklabels(product_categories)
    ax.set_xlabel('Product Category')
    ax.set_title('Brand Awareness by Product Category')

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Awareness')

    ax.yaxis.set_visible(False)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    satisfaction_vs_recommendation_bar()
    dissatisfaction_bar_chart()
    product_awareness_bar_chart()
    product_awareness_bar_chart_percent()