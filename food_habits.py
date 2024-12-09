import matplotlib.pyplot as plt


def favorite_food():
    labels = ['Yes', 'No']
    values = [3, 1]
    colors = ['forestgreen', 'lightcoral']

    plt.figure(figsize=(8, 6))
    wedges, texts = plt.pie(
        values,
        labels=labels,
        startangle=90,
        colors=colors,
        textprops={'fontsize': 12},
        wedgeprops={'width': 0.3}
    )

    plt.text(0, -1.4, "Yes = 3, No = 1", ha='center', va='center', fontsize=12, color='black')

    plt.title("Is the favorite food of participants from their home country?", fontsize=14)
    plt.show()

def favorite_food_leaning_traditional():
    categories = ['Yes', 'No']
    values = [4, 0]
    colors = ['forestgreen', 'lightcoral']

    plt.figure(figsize=(8, 6))
    bars = plt.bar(categories, values, color=colors)

    plt.title("Is Their Favorite Food a Traditional Food?", fontsize=16)
    plt.xticks(fontsize=12)
    plt.gca().axes.yaxis.set_visible(False)

    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    for bar, label in zip(bars, categories):
        value = int(bar.get_height())
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 str(value), ha='center', fontsize=12, color='black')

    plt.show()

def responsiblity_for_cooking():
    labels = ['Mother', 'Shared Cooking']
    values = [2, 2]
    colors = ['DarkSalmon', 'Seagreen']

    plt.figure(figsize=(8, 6))
    wedges, texts, autotexts = plt.pie(
        values,
        labels=labels,
        autopct=lambda pct: f'{int(pct * sum(values) / 100)}',
        startangle=90,
        colors=colors,
        textprops={'fontsize': 12}
    )
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(12)

    plt.title("Who Was Responsible for Preparing Meals When They Lived with Their Family?", fontsize=14)
    plt.show()

def currently_prepare_meals_themselves():
    labels = ['Yes', 'No']
    values = [2, 2]
    colors = ['forestgreen', 'lightcoral']

    plt.figure(figsize=(8, 6))
    wedges, texts, autotexts = plt.pie(
        values,
        labels=labels,
        autopct=lambda pct: f'{int(pct * sum(values) / 100)}',
        startangle=90,
        colors=colors,
        textprops={'fontsize': 12}
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)

    plt.title("Do Participants Currently Prepare Meals by Themselves?", fontsize=14)
    plt.show()

if __name__ == '__main__':
    favorite_food()
    favorite_food_leaning_traditional()
    responsiblity_for_cooking()
    currently_prepare_meals_themselves()
