import pandas as pd
import matplotlib.pyplot as plt

data_csv = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech_Copy.csv")


def qualities_that_satisfy_pie():
    data = {
        'Qualities': ['Ease of use', 'Value for money', 'Features', 'Durability', 'Performance'],
        'Mouse': [14, 5, 3, 12, 15],
        'Keyboard': [3, 1, 1, 1, 2],
        'Webcam': [2, 1, 0, 2, 1],
        'Controller': [0, 1, 1, 1, 2],
        'Headset': [1, 0, 0, 1, 0],
        'Mousepad': [0, 0, 0, 1, 1]
    }
    df = pd.DataFrame(data)

    df.set_index('Qualities', inplace=True)

    total_satisfaction = df.sum(axis=1)

    total_responses = total_satisfaction.sum()
    percent_satisfaction = (total_satisfaction / total_responses) * 100

    percent_satisfaction = percent_satisfaction.sort_values()

    plt.figure(figsize=(8, 8))
    plt.pie(percent_satisfaction, labels=percent_satisfaction.index, autopct='%1.1f%%', startangle=90,
            colors=plt.cm.Paired.colors, pctdistance=0.85)
    plt.title('Qualities people are satisfied with accross all products')
    plt.show()


def qualities_that_dissatisfy_pie():
    dissatisfied_data = {
        'Qualities': ['Ease of use', 'Value for money', 'Features', 'Durability', 'Performance'],
        'Mouse': [1, 6, 3, 2, 2],
        'Keyboard': [0, 1, 1, 0, 0],
        'Webcam': [0, 0, 2, 0, 0],
        'Controller': [0, 1, 0, 0, 0],
        'Mousepad': [0, 1, 0, 0, 0]
    }

    df_dissatisfied = pd.DataFrame(dissatisfied_data)
    df_dissatisfied.set_index('Qualities', inplace=True)
    total_dissatisfaction = df_dissatisfied.sum(axis=1)
    total_responses_dissatisfied = total_dissatisfaction.sum()

    percent_dissatisfaction = (total_dissatisfaction / total_responses_dissatisfied) * 100
    percent_dissatisfaction = percent_dissatisfaction.sort_values()

    plt.figure(figsize=(8, 8))
    plt.pie(percent_dissatisfaction, labels=percent_dissatisfaction.index, autopct='%1.1f%%', startangle=90,
            colors=plt.cm.Paired.colors)
    plt.title('Qualities people are dissatisfied with accross all products')
    plt.show()


def satisfied_vs_dissatisfied_total_answers():
    total_responses = 28
    satisfied_responses = 28
    dissatisfied_responses = 14

    percent_satisfied = (satisfied_responses / total_responses) * 100
    percent_dissatisfied = (dissatisfied_responses / total_responses) * 100

    labels = ['What qualities are you satisfied with?', 'What qualities are you dissatisfied with?']
    percentages = [percent_satisfied, percent_dissatisfied]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, percentages, color=['skyblue', 'tomato'])
    plt.xlabel('Question Type')
    plt.ylabel('Percentage of all Users')
    plt.title('Percentage of users answering satisfaction vs dissatisfaction questions')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.1f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


def support_type_pie():
    issue_contact_column = 'If you ever had an issue with your logitech product whom did you contact your retailer or logitech customer service?'

    issue_contact_counts = data_csv[issue_contact_column].value_counts()

    colors = {
        "I never had an issue with my product": "lightgreen",
        "Customer service": "tomato",
        "Retailer": "skyblue"
    }

    color_list = [colors[label] for label in issue_contact_counts.index]

    explode = [0.1 if (count / issue_contact_counts.sum()) < 0.05 else 0 for count in issue_contact_counts]

    # Plotting the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(issue_contact_counts, labels=issue_contact_counts.index, autopct='%1.1f%%', startangle=90,
            colors=color_list, explode=explode, pctdistance=0.85)
    plt.title('Contact for Issues with Logitech Product')
    plt.show()
    plt.show()


def recommendation_pie():
    data = data_csv
    data.columns = data.columns.str.strip()

    recommendation_column = 'How likely are you to recommend Logitech products to others?'
    recommendation_counts = data[recommendation_column].value_counts()

    colors_recommendation = {
        "Likely": "forestgreen",
        "Unlikely": "tomato",
        "It depends": "skyblue"
    }

    color_list_recommendation = [colors_recommendation[label] for label in recommendation_counts.index]

    explode_recommendation = [0.1 if (count / recommendation_counts.sum()) < 0.05 else 0 for count in
                              recommendation_counts]

    plt.figure(figsize=(8, 8))
    plt.pie(recommendation_counts, labels=recommendation_counts.index, autopct='%1.1f%%', startangle=90,
            colors=color_list_recommendation, explode=explode_recommendation, pctdistance=0.85)
    plt.title('Likelihood of Recommending Logitech Products')
    plt.show()


def recommendation_with_vs_without_issues_bar():
    data = data_csv
    data.columns = data.columns.str.strip()

    issue_contact_column = 'If you ever had an issue with your logitech product whom did you contact your retailer or logitech customer service?'
    recommendation_column = 'How likely are you to recommend Logitech products to others?'

    issue_data = data[data[issue_contact_column] != 'I never had an issue with my product']
    no_issue_data = data[data[issue_contact_column] == 'I never had an issue with my product']

    recommendation_counts_with_issues = issue_data[recommendation_column].value_counts(normalize=True) * 100
    recommendation_counts_without_issues = no_issue_data[recommendation_column].value_counts(normalize=True) * 100
    recommendation_counts_with_issues = recommendation_counts_with_issues.reindex(['Likely', 'Unlikely', 'It depends'],
                                                                                  fill_value=0)
    recommendation_counts_without_issues = recommendation_counts_without_issues.reindex(
        ['Likely', 'Unlikely', 'It depends'], fill_value=0)

    recommendation_df = pd.DataFrame({
        'With Issues': recommendation_counts_with_issues,
        'Without Issues': recommendation_counts_without_issues
    })

    colors = ['tomato', 'forestgreen', 'skyblue']

    ax = recommendation_df.plot(kind='bar', figsize=(10, 6), color=colors)
    ax.set_title('Likelihood of Recommending Logitech Products')
    ax.legend(title='Issues')
    ax.yaxis.set_visible(False)

    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', label_type='edge')

    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def bar_likelihood_of_recommending_issue_vs_no_issue():
    data = data_csv
    data.columns = data.columns.str.strip()

    issue_contact_column = 'If you ever had an issue with your logitech product whom did you contact your retailer or logitech customer service?'
    recommendation_column = 'How likely are you to recommend Logitech products to others?'

    issue_data = data[data[issue_contact_column] != 'I never had an issue with my product']
    no_issue_data = data[data[issue_contact_column] == 'I never had an issue with my product']

    recommendation_counts_with_issues = issue_data[recommendation_column].value_counts(normalize=True) * 100
    recommendation_counts_without_issues = no_issue_data[recommendation_column].value_counts(normalize=True) * 100

    recommendation_counts_with_issues = recommendation_counts_with_issues.reindex(['Likely', 'Unlikely', 'It depends'],
                                                                                  fill_value=0)
    recommendation_counts_without_issues = recommendation_counts_without_issues.reindex(
        ['Likely', 'Unlikely', 'It depends'], fill_value=0)

    recommendation_df = pd.DataFrame({
        'With Issues': recommendation_counts_with_issues,
        'Without Issues': recommendation_counts_without_issues
    })

    colors = {
        'Likely': 'forestgreen',
        'Unlikely': 'tomato',
        'It depends': 'skyblue'
    }

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.barh('With Issues', recommendation_df.loc['Likely', 'With Issues'], color=colors['Likely'])
    ax.barh('With Issues', recommendation_df.loc['Unlikely', 'With Issues'],
            left=recommendation_df.loc['Likely', 'With Issues'], color=colors['Unlikely'])
    ax.barh('With Issues', recommendation_df.loc['It depends', 'With Issues'],
            left=recommendation_df.loc['Likely', 'With Issues'] + recommendation_df.loc['Unlikely', 'With Issues'],
            color=colors['It depends'])

    ax.barh('Without Issues', recommendation_df.loc['Likely', 'Without Issues'], color=colors['Likely'])
    ax.barh('Without Issues', recommendation_df.loc['Unlikely', 'Without Issues'],
            left=recommendation_df.loc['Likely', 'Without Issues'], color=colors['Unlikely'])
    ax.barh('Without Issues', recommendation_df.loc['It depends', 'Without Issues'],
            left=recommendation_df.loc['Likely', 'Without Issues'] + recommendation_df.loc[
                'Unlikely', 'Without Issues'], color=colors['It depends'])

    for label, color in colors.items():
        for i, category in enumerate(recommendation_df.columns):
            value = recommendation_df.loc[label, category]
            if value > 0:
                text = f'{int(value)}%' if value.is_integer() else f'{value:.1f}%'
                ax.text(sum(recommendation_df.loc[:label, category]) - value / 2, category, text, va='center',
                        ha='center', color='white', fontweight='bold')

    ax.set_xlim(0, 100)
    ax.set_xticks(range(0, 101, 10))
    ax.set_xlabel('Percentage')
    ax.set_title('Likelihood of Recommending Logitech Products')
    ax.legend(['Likely', 'Unlikely', 'It depends'], loc='best')
    plt.tight_layout()
    plt.show()


def overall_satisfaction_bar():
    data = data_csv
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

    issue_contact_column = 'If you ever had an issue with your logitech product whom did you contact your retailer or logitech customer service?'

    issue_data = data[data[issue_contact_column] != 'I never had an issue with my product']
    no_issue_data = data[data[issue_contact_column] == 'I never had an issue with my product']

    satisfaction_counts_with_issues = issue_data['Overall Satisfaction Label'].value_counts()
    satisfaction_counts_without_issues = no_issue_data['Overall Satisfaction Label'].value_counts()

    satisfaction_percentages_with_issues = satisfaction_counts_with_issues / satisfaction_counts_with_issues.sum() * 100
    satisfaction_percentages_without_issues = satisfaction_counts_without_issues / satisfaction_counts_without_issues.sum() * 100

    explode_with_issues = (satisfaction_percentages_with_issues < 5).astype(float) * 0.1
    explode_without_issues = (satisfaction_percentages_without_issues < 5).astype(float) * 0.1

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    axes[0].pie(satisfaction_counts_with_issues, labels=satisfaction_counts_with_issues.index, autopct='%1.1f%%',
                                           startangle=90, colors=plt.cm.Pastel1.colors, explode=explode_with_issues, pctdistance=0.85)
    axes[0].set_title('Overall Satisfaction (With Issues)')
    axes[0].axis('equal')

    axes[1].pie(satisfaction_counts_without_issues, labels=satisfaction_counts_without_issues.index, autopct='%1.1f%%',
                                           startangle=90, colors=plt.cm.Pastel2.colors, explode=explode_without_issues, pctdistance=0.85)
    axes[1].set_title('Overall Satisfaction (Without Issues)')
    axes[1].axis('equal')

    plt.tight_layout()
    plt.show()


def satisfaction_vs_recommendation():
    data = data_csv
    satisfaction_columns = [col for col in data.columns if col.startswith('How satisfied are you with your')]

    data['Overall Satisfaction'] = data[satisfaction_columns].mean(axis=1).round()

    high_satisfaction_data = data[data['Overall Satisfaction'] >= 4]

    recommendation_column = 'How likely are you to recommend Logitech products to others?'
    recommendation_counts = high_satisfaction_data[recommendation_column].value_counts(normalize=True) * 100

    colors = ['forestgreen', 'skyblue']

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(recommendation_counts.index, recommendation_counts, color=colors)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.1f}%', ha='center', va='bottom')

    ax.set_xlabel('Likelihood to Recommend')
    ax.set_ylabel('Percentage')
    ax.set_title('Likelihood to Recommend Logitech Products (Satisfaction Score 4 or More)')
    plt.xticks(rotation=0)

    plt.tight_layout()
    plt.show()


def satisfaction_vs_recommendation_double_pie():
    data = data_csv
    satisfaction_columns = [col for col in data.columns if col.startswith('How satisfied are you with your')]

    data['Overall Satisfaction'] = data[satisfaction_columns].mean(axis=1).round()

    high_satisfaction_data = data[data['Overall Satisfaction'] >= 4]
    low_satisfaction_data = data[data['Overall Satisfaction'] < 4]

    recommendation_column = 'How likely are you to recommend Logitech products to others?'

    recommendation_counts_high = high_satisfaction_data[recommendation_column].value_counts()
    recommendation_counts_low = low_satisfaction_data[recommendation_column].value_counts()

    colors = {
        'Likely': 'forestgreen',
        'Unlikely': 'tomato',
        'It depends': 'skyblue'
    }

    recommendation_percentages_high = recommendation_counts_high / recommendation_counts_high.sum() * 100
    recommendation_percentages_low = recommendation_counts_low / recommendation_counts_low.sum() * 100

    explode_high = (recommendation_percentages_high < 5).astype(float) * 0.1
    explode_low = (recommendation_percentages_low < 5).astype(float) * 0.1

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    axes[0].pie(recommendation_counts_high, labels=recommendation_counts_high.index, autopct='%1.1f%%',
                                           startangle=90, colors=[colors[label] for label in recommendation_counts_high.index], explode=explode_high, pctdistance=0.85)
    axes[0].set_title('Recommendation (Satisfaction Score 4 or More)')
    axes[0].axis('equal')

    axes[1].pie(recommendation_counts_low, labels=recommendation_counts_low.index, autopct='%1.1f%%',
                                           startangle=90, colors=[colors[label] for label in recommendation_counts_low.index], explode=explode_low, pctdistance=0.85)
    axes[1].set_title('Recommendation (Satisfaction Score Less Than 4)')
    axes[1].axis('equal')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    qualities_that_satisfy_pie()
    qualities_that_dissatisfy_pie()
    support_type_pie()
    recommendation_pie()
    recommendation_with_vs_without_issues_bar()
    bar_likelihood_of_recommending_issue_vs_no_issue()
    overall_satisfaction_bar()
    satisfaction_vs_recommendation()
    satisfaction_vs_recommendation_double_pie()