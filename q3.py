import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

def create_pie_percentual():
    data = pd.read_csv(r"C:\Users\green\PycharmProjects\statisticsPython\logitech_csv\Modified_Logitech.csv")

    # Assuming the column name is exactly 'Were you aware that the product was made by Logitech when you purchased it?'
    # Check your actual column names and adjust if necessary
    awareness_counts = data['Were you aware that the product was made by Logitech when you purchased it?'].value_counts()

    # Plotting the data
    fig, ax = plt.subplots()
    ax.pie(awareness_counts, labels=awareness_counts.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'tomato'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title('Awareness of Logitech Brand at Purchase')
    plt.show()

if __name__ == '__main__':
    create_pie_percentual()