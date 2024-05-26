from io import StringIO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from statsmodels.stats.proportion import proportion_confint

data_csv_raw = """
Timestamp,How old are you?,Do you use any Logitech products?,Were you aware that the product was made by Logitech when you purchased it?,How long have you been a user or owner of a Logitech product?,What Logitech Product do you use the most?,How satisfied are you with your Logitech mouse?,What qualities are you satisfied with? ,What qualities are you dissatisfied with? ,How satisfied are you with your Logitech keyboard?,What qualities are you satisfied with? .1,What qualities are you dissatisfied with? .1,How satisfied are you with your Logitech webcam?,What qualities are you satisfied with? .2,What qualities are you dissatisfied with? .2,How satisfied are you with your Logitech headset?,What qualities are you satisfied with? .3,What qualities are you dissatisfied with? .3,How satisfied are you with your Logitech speakers?,What qualities are you satisfied with? .4,What qualities are you dissatisfied with? .4,How satisfied are you with your Logitech product?,What qualities are you satisfied with? .5,What qualities are you dissatisfied with? .5,If you ever had an issue with your logitech product whom did you contact your retailer or logitech customer service?,Were you satisfied with Logitech customer service?,How likely are you to recommend Logitech products to others?
2024/03/04 3:18:36 pm EET,21-30,Yes,Yes,More than 3 years,Mouse,5,Durability,,,,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/03/04 3:28:40 pm EET,16-20,Yes,Yes,More than 3 years,Webcam,,,,,,,4,Ease of use;Durability,Features,,,,,,,,,,I never had an issue with my product,,Likely
2024/03/04 3:29:31 pm EET,21-30,Yes,Yes,More than 3 years,Keyboard,,,,,,,,,,,,,,,,3,Ease of use;Value for money,Features,I never had an issue with my product,,Unlikely
2024/03/04 4:55:14 pm EET,16-20,No,,,,,,,,,,,,,,,,,,,,,,,,
2024/03/04 4:58:54 pm EET,21-30,Yes,No,More than 3 years,Mouse,3,Ease of use;Durability,Value for money;Performance,,,,,,,,,,,,,,,,I never had an issue with my product,,It depends
2024/03/04 6:28:19 pm EET,55+,Yes,Yes,More than 3 years,Mouse,5,Ease of use;Value for money;Durability;Performance,,,,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/03/04 8:59:00 pm EET,21-30,Yes,Yes,Less than 6 months,Mouse,5,Features;Performance,,,,,,,,,,,,,,,,,I never had an issue with my product,,It depends
2024/03/05 3:27:40 am EET,21-30,Yes,Yes,More than 3 years,Game Controller,,,,,,,,,,,,,,,,5,Durability;Performance,Value for money,I never had an issue with my product,,Likely
2024/03/05 1:00:44 pm EET,21-30,Yes,Yes,More than 3 years,Game Controller,,,,,,,,,,,,,,,,5,Value for money;Features;Performance,,I never had an issue with my product,,It depends
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
2024/04/15 12:54:17 pm EET,21-30,Yes,Yes,More than 3 years,Keyboard,,,,,,,,,,,,,,,,5,Ease of use;Features;Durability;Performance,Value for money,Retailer,,Likely
2024/04/15 12:56:08 pm EET,16-20,Yes,Yes,More than 3 years,Mouse,5,Ease of use;Durability;Performance,,,,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/04/15 2:00:58 pm EET,16-20,No,,,,,,,,,,,,,,,,,,,,,,,,
2024/04/15 2:31:33 pm EET,21-30,Yes,Yes,1-3 years,Mouse,4,Ease of use;Value for money;Durability,Features,,,,,,,,,,,,,,,,I never had an issue with my product,,It depends
2024/04/15 4:44:46 pm EET,21-30,Yes,Yes,More than 3 years,Mouse,5,Ease of use;Features;Performance,,,,,,,,,,,,,,,,,Customer service,Yes,Likely
2024/04/15 6:44:24 pm EET,21-30,Yes,Yes,1-3 years,Keyboard,,,,5,Ease of use;Performance,,,,,,,,,,,,,,I never had an issue with my product,,Likely
2024/05/06 1:57:48 pm EEST,16-20,Yes,Yes,More than 3 years,Webcam,,,,,,,5,Ease of use;Value for money;Durability;Performance,Features,,,,,,,,,,Retailer,,Likely
"""

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

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Set the qualities as the index
    df.set_index('Qualities', inplace=True)

    # Sum the satisfaction counts for each quality across all product categories
    total_satisfaction = df.sum(axis=1)

    # Calculate the percentage for each quality
    total_responses = total_satisfaction.sum()
    percent_satisfaction = (total_satisfaction / total_responses) * 100

    # Sort the percentage satisfaction in ascending order
    percent_satisfaction = percent_satisfaction.sort_values()

    # Plotting the pie chart
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

    # Convert the data to a pandas DataFrame
    df_dissatisfied = pd.DataFrame(dissatisfied_data)

    # Set the qualities as the index
    df_dissatisfied.set_index('Qualities', inplace=True)

    # Sum the dissatisfaction counts for each quality across all product categories
    total_dissatisfaction = df_dissatisfied.sum(axis=1)

    # Calculate the percentage for each quality
    total_responses_dissatisfied = total_dissatisfaction.sum()
    percent_dissatisfaction = (total_dissatisfaction / total_responses_dissatisfied) * 100

    # Sort the percentage dissatisfaction in ascending order
    percent_dissatisfaction = percent_dissatisfaction.sort_values()

    # Plotting the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(percent_dissatisfaction, labels=percent_dissatisfaction.index, autopct='%1.1f%%', startangle=90,
            colors=plt.cm.Paired.colors)
    plt.title('Qualities people are dissatisfied with accross all products')
    plt.show()

def staisfied_vs_dissatisified_total_answers():
    total_responses = 28
    satisfied_responses = 28  # Assuming all 28 answered the satisfaction question
    dissatisfied_responses = 14  # From the previous data

    # Calculate percentages
    percent_satisfied = (satisfied_responses / total_responses) * 100
    percent_dissatisfied = (dissatisfied_responses / total_responses) * 100
    percent_no_dissatisfaction = 100 - percent_dissatisfied

    # Data for the bar chart
    labels = ['What qualities are you satisfied with?', 'What qualities are you dissatisfied with?']
    percentages = [percent_satisfied, percent_dissatisfied]

    # Plotting the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, percentages, color=['skyblue', 'tomato'])
    plt.xlabel('Question Type')
    plt.ylabel('Percentage of all Users')
    plt.title('Percentage of users answering satisfaction vs dissatisfaction questions')

    # Adding percentage labels on top of the bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.1f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

def support_type_pie():
    data_csv = pd.read_csv(StringIO(data_csv_raw))

    # Extract the relevant column for the question about contacting retailer or customer service
    issue_contact_column = 'If you ever had an issue with your logitech product whom did you contact your retailer or logitech customer service?'

    # Count the occurrences of each response
    issue_contact_counts = data_csv[issue_contact_column].value_counts()

    # Define colors for the slices
    colors = {
        "I never had an issue with my product": "lightgreen",
        "Customer service": "tomato",
        "Retailer": "skyblue"
    }

    # Ensure colors are mapped in the correct order
    color_list = [colors[label] for label in issue_contact_counts.index]

    # Calculate explode parameters to explode slices < 5%
    explode = [0.1 if (count / issue_contact_counts.sum()) < 0.05 else 0 for count in issue_contact_counts]

    # Plotting the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(issue_contact_counts, labels=issue_contact_counts.index, autopct='%1.1f%%', startangle=90,
            colors=color_list, explode=explode, pctdistance=0.85)
    plt.title('Contact for Issues with Logitech Product')
    plt.show()
    plt.show()

def recommendation_pie():
    data = pd.read_csv(StringIO(data_csv_raw))

    # Clean column names by stripping leading and trailing spaces
    data.columns = data.columns.str.strip()

    # Extract the relevant column for the question about recommending Logitech products
    recommendation_column = 'How likely are you to recommend Logitech products to others?'

    # Count the occurrences of each response
    recommendation_counts = data[recommendation_column].value_counts()

    # Define the color scheme
    colors_recommendation = {
        "Likely": "forestgreen",
        "Unlikely": "tomato",
        "It depends": "skyblue"
    }

    # Ensure colors are mapped in the correct order
    color_list_recommendation = [colors_recommendation[label] for label in recommendation_counts.index]

    # Calculate explode parameters to explode slices < 5%
    explode_recommendation = [0.1 if (count / recommendation_counts.sum()) < 0.05 else 0 for count in
                              recommendation_counts]

    # Plotting the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(recommendation_counts, labels=recommendation_counts.index, autopct='%1.1f%%', startangle=90,
            colors=color_list_recommendation, explode=explode_recommendation, pctdistance=0.85)
    plt.title('Likelihood of Recommending Logitech Products')
    plt.show()

def recommendation_with_vs_without_issues_bar():
    data = pd.read_csv(StringIO(data_csv_raw))

    # Clean column names by stripping leading and trailing spaces
    data.columns = data.columns.str.strip()

    # Extract relevant columns
    issue_contact_column = 'If you ever had an issue with your logitech product whom did you contact your retailer or logitech customer service?'
    recommendation_column = 'How likely are you to recommend Logitech products to others?'

    # Filter data for those who had an issue
    issue_data = data[data[issue_contact_column] != 'I never had an issue with my product']
    no_issue_data = data[data[issue_contact_column] == 'I never had an issue with my product']

    # Count the occurrences of each recommendation response
    recommendation_counts_with_issues = issue_data[recommendation_column].value_counts(normalize=True) * 100
    recommendation_counts_without_issues = no_issue_data[recommendation_column].value_counts(normalize=True) * 100

    # Sort the indices to align both series
    recommendation_counts_with_issues = recommendation_counts_with_issues.reindex(['Likely', 'Unlikely', 'It depends'],
                                                                                  fill_value=0)
    recommendation_counts_without_issues = recommendation_counts_without_issues.reindex(
        ['Likely', 'Unlikely', 'It depends'], fill_value=0)

    # Create a DataFrame for plotting
    recommendation_df = pd.DataFrame({
        'With Issues': recommendation_counts_with_issues,
        'Without Issues': recommendation_counts_without_issues
    })

    # Define colors
    colors = ['tomato', 'forestgreen', 'skyblue']

    # Plotting the bar chart
    ax = recommendation_df.plot(kind='bar', figsize=(10, 6), color=colors)
    ax.set_title('Likelihood of Recommending Logitech Products')
    ax.legend(title='Issues')
    ax.yaxis.set_visible(False)

    # Adding percentage labels on top of the bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', label_type='edge')

    plt.xticks(rotation=0)
    plt.tight_layout()

    # Show the plot
    plt.show()

def bar_likelihood_of_recommending_issue_vs_no_issue():
    data = pd.read_csv(StringIO(data_csv_raw))

    # Clean column names by stripping leading and trailing spaces
    data.columns = data.columns.str.strip()

    # Extract relevant columns
    issue_contact_column = 'If you ever had an issue with your logitech product whom did you contact your retailer or logitech customer service?'
    recommendation_column = 'How likely are you to recommend Logitech products to others?'

    # Filter data for those who had an issue
    issue_data = data[data[issue_contact_column] != 'I never had an issue with my product']
    no_issue_data = data[data[issue_contact_column] == 'I never had an issue with my product']

    # Count the occurrences of each recommendation response
    recommendation_counts_with_issues = issue_data[recommendation_column].value_counts(normalize=True) * 100
    recommendation_counts_without_issues = no_issue_data[recommendation_column].value_counts(normalize=True) * 100

    # Sort the indices to align both series
    recommendation_counts_with_issues = recommendation_counts_with_issues.reindex(['Likely', 'Unlikely', 'It depends'],
                                                                                  fill_value=0)
    recommendation_counts_without_issues = recommendation_counts_without_issues.reindex(
        ['Likely', 'Unlikely', 'It depends'], fill_value=0)

    # Create a DataFrame for plotting
    recommendation_df = pd.DataFrame({
        'With Issues': recommendation_counts_with_issues,
        'Without Issues': recommendation_counts_without_issues
    })

    # Define colors
    colors = {
        'Likely': 'forestgreen',
        'Unlikely': 'tomato',
        'It depends': 'skyblue'
    }

    # Plotting the stacked bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot bars for 'With Issues'
    ax.barh('With Issues', recommendation_df.loc['Likely', 'With Issues'], color=colors['Likely'])
    ax.barh('With Issues', recommendation_df.loc['Unlikely', 'With Issues'],
            left=recommendation_df.loc['Likely', 'With Issues'], color=colors['Unlikely'])
    ax.barh('With Issues', recommendation_df.loc['It depends', 'With Issues'],
            left=recommendation_df.loc['Likely', 'With Issues'] + recommendation_df.loc['Unlikely', 'With Issues'],
            color=colors['It depends'])

    # Plot bars for 'Without Issues'
    ax.barh('Without Issues', recommendation_df.loc['Likely', 'Without Issues'], color=colors['Likely'])
    ax.barh('Without Issues', recommendation_df.loc['Unlikely', 'Without Issues'],
            left=recommendation_df.loc['Likely', 'Without Issues'], color=colors['Unlikely'])
    ax.barh('Without Issues', recommendation_df.loc['It depends', 'Without Issues'],
            left=recommendation_df.loc['Likely', 'Without Issues'] + recommendation_df.loc[
                'Unlikely', 'Without Issues'], color=colors['It depends'])

    # Adding percentage labels in the middle of the bars
    for label, color in colors.items():
        for i, category in enumerate(recommendation_df.columns):
            value = recommendation_df.loc[label, category]
            if value > 0:
                text = f'{int(value)}%' if value.is_integer() else f'{value:.1f}%'
                ax.text(sum(recommendation_df.loc[:label, category]) - value / 2, category, text, va='center',
                        ha='center', color='white', fontweight='bold')

    # Set labels
    ax.set_xlim(0, 100)
    ax.set_xticks(range(0, 101, 10))
    ax.set_xlabel('Percentage')
    ax.set_title('Likelihood of Recommending Logitech Products')
    ax.legend(['Likely', 'Unlikely', 'It depends'], loc='best')

    plt.tight_layout()
    plt.show()

def overall_satisfaction_bar():
    data = pd.read_csv(StringIO(data_csv_raw))
    satisfaction_columns = [col for col in data.columns if col.startswith('How satisfied are you with your')]

    # Calculate the average satisfaction score for each respondent
    data['Overall Satisfaction'] = data[satisfaction_columns].mean(axis=1).round()

    # Map numerical scores to textual labels
    satisfaction_labels = {
        1.0: 'Very Dissatisfied',
        2.0: 'Dissatisfied',
        3.0: 'Neutral',
        4.0: 'Satisfied',
        5.0: 'Very Satisfied'
    }
    data['Overall Satisfaction Label'] = data['Overall Satisfaction'].map(satisfaction_labels)

    # Extract relevant column for issue
    issue_contact_column = 'If you ever had an issue with your logitech product whom did you contact your retailer or logitech customer service?'

    # Filter data for those who had and did not have an issue
    issue_data = data[data[issue_contact_column] != 'I never had an issue with my product']
    no_issue_data = data[data[issue_contact_column] == 'I never had an issue with my product']

    # Count the occurrences of each satisfaction level for both groups
    satisfaction_counts_with_issues = issue_data['Overall Satisfaction Label'].value_counts()
    satisfaction_counts_without_issues = no_issue_data['Overall Satisfaction Label'].value_counts()

    # Calculate the percentage for each slice to determine explosion
    satisfaction_percentages_with_issues = satisfaction_counts_with_issues / satisfaction_counts_with_issues.sum() * 100
    satisfaction_percentages_without_issues = satisfaction_counts_without_issues / satisfaction_counts_without_issues.sum() * 100

    # Determine slices to explode: explode if less than 5%
    explode_with_issues = (satisfaction_percentages_with_issues < 5).astype(float) * 0.1
    explode_without_issues = (satisfaction_percentages_without_issues < 5).astype(float) * 0.1

    # Create pie charts
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    wedges, texts, autotexts = axes[0].pie(satisfaction_counts_with_issues, labels=satisfaction_counts_with_issues.index, autopct='%1.1f%%',
                                           startangle=90, colors=plt.cm.Pastel1.colors, explode=explode_with_issues, pctdistance=0.85)
    axes[0].set_title('Overall Satisfaction (With Issues)')
    axes[0].axis('equal')

    wedges, texts, autotexts = axes[1].pie(satisfaction_counts_without_issues, labels=satisfaction_counts_without_issues.index, autopct='%1.1f%%',
                                           startangle=90, colors=plt.cm.Pastel2.colors, explode=explode_without_issues, pctdistance=0.85)
    axes[1].set_title('Overall Satisfaction (Without Issues)')
    axes[1].axis('equal')

    plt.tight_layout()
    plt.show()


def satisfaction_vs_recommendation():
    data = pd.read_csv(StringIO(data_csv_raw))
    # Filter columns related to satisfaction
    satisfaction_columns = [col for col in data.columns if col.startswith('How satisfied are you with your')]

    # Calculate the average satisfaction score for each respondent
    data['Overall Satisfaction'] = data[satisfaction_columns].mean(axis=1).round()

    # Filter data for those who gave a score of 4 or more
    high_satisfaction_data = data[data['Overall Satisfaction'] >= 4]

    # Extract the relevant column for recommendation
    recommendation_column = 'How likely are you to recommend Logitech products to others?'

    # Count the occurrences of each recommendation response for those with high satisfaction
    recommendation_counts = high_satisfaction_data[recommendation_column].value_counts(normalize=True) * 100

    # Define colors
    colors = ['forestgreen', 'skyblue']

    # Plotting the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(recommendation_counts.index, recommendation_counts, color=colors)

    # Adding percentage labels on top of the bars
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
    data = pd.read_csv(StringIO(data_csv_raw))
    satisfaction_columns = [col for col in data.columns if col.startswith('How satisfied are you with your')]

    # Calculate the average satisfaction score for each respondent
    data['Overall Satisfaction'] = data[satisfaction_columns].mean(axis=1).round()

    # Filter data for those who gave a score of 4 or more
    high_satisfaction_data = data[data['Overall Satisfaction'] >= 4]

    # Filter data for those who gave a score of less than 4
    low_satisfaction_data = data[data['Overall Satisfaction'] < 4]

    # Extract the relevant column for recommendation
    recommendation_column = 'How likely are you to recommend Logitech products to others?'

    # Count the occurrences of each recommendation response for those with high satisfaction
    recommendation_counts_high = high_satisfaction_data[recommendation_column].value_counts()
    recommendation_counts_low = low_satisfaction_data[recommendation_column].value_counts()

    # Define colors
    colors = {
        'Likely': 'forestgreen',
        'Unlikely': 'tomato',
        'It depends': 'skyblue'
    }

    # Calculate the percentage for each slice to determine explosion
    recommendation_percentages_high = recommendation_counts_high / recommendation_counts_high.sum() * 100
    recommendation_percentages_low = recommendation_counts_low / recommendation_counts_low.sum() * 100

    # Determine slices to explode: explode if less than 5%
    explode_high = (recommendation_percentages_high < 5).astype(float) * 0.1
    explode_low = (recommendation_percentages_low < 5).astype(float) * 0.1

    # Create pie charts
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    wedges, texts, autotexts = axes[0].pie(recommendation_counts_high, labels=recommendation_counts_high.index, autopct='%1.1f%%',
                                           startangle=90, colors=[colors[label] for label in recommendation_counts_high.index], explode=explode_high, pctdistance=0.85)
    axes[0].set_title('Recommendation (Satisfaction Score 4 or More)')
    axes[0].axis('equal')

    wedges, texts, autotexts = axes[1].pie(recommendation_counts_low, labels=recommendation_counts_low.index, autopct='%1.1f%%',
                                           startangle=90, colors=[colors[label] for label in recommendation_counts_low.index], explode=explode_low, pctdistance=0.85)
    axes[1].set_title('Recommendation (Satisfaction Score Less Than 4)')
    axes[1].axis('equal')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # qualities_that_satisfy_pie()
    # qualities_that_dissatisfy_pie()
    # staisfied_vs_dissatisified_total_answers()
    # support_type_pie()
    # recommendation_pie()
    # recommendation_with_vs_without_issues_bar()
    # bar_likelihood_of_recommending_issue_vs_no_issue()
    # overall_satisfaction_bar()
    satisfaction_vs_recommendation()
    satisfaction_vs_recommendation_double_pie()