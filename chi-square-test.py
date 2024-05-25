import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import chi2

def perform_chi_square():
    observed_yes = np.array([19, 3, 2, 2])
    observed_no = np.array([2, 0, 0, 0])

    # Total counts
    total_yes = np.sum(observed_yes)
    total_no = np.sum(observed_no)
    total = total_yes + total_no

    # Calculate expected frequencies
    expected_yes = (total_yes / total) * (observed_yes + observed_no)
    expected_no = (total_no / total) * (observed_yes + observed_no)

    # Calculate chi-square statistic for non-zero expected values
    chi_square_yes = np.sum((observed_yes - expected_yes) ** 2 / expected_yes)
    chi_square_no = np.sum((observed_no - expected_no) ** 2 / expected_no)

    # Total chi-square statistic
    chi_square_total = chi_square_yes + chi_square_no

    # Degrees of freedom
    df = (len(observed_yes) - 1) * 1  # 1 row in this context (Yes/No), 4 columns (products)

    # P-value from chi-square distribution
    p_value = 1 - chi2.cdf(chi_square_total, df)

    # Critical value for 95% confidence level
    critical_value = chi2.ppf(0.95, df)

    print(
        f"Chi-Square Total: {chi_square_total}, Degrees of Freedom: {df}, P-Value: {p_value}, Critical Value: {critical_value}")


def visualize_chi_square_results():
    # Observed frequencies
    observed_yes = np.array([19, 3, 2, 2])
    observed_no = np.array([2, 0, 0, 0])

    # Total counts
    total_yes = np.sum(observed_yes)
    total_no = np.sum(observed_no)
    total = total_yes + total_no

    # Calculate expected frequencies
    expected_yes = (total_yes / total) * (observed_yes + observed_no)
    expected_no = (total_no / total) * (observed_yes + observed_no)

    # Create labels for products
    products = ['Mouse', 'Keyboard', 'Controller', 'Webcam']

    # Bar width
    bar_width = 0.35

    # Positions of the bars on the x-axis
    r1 = np.arange(len(products))
    r2 = [x + bar_width for x in r1]

    # Create the bar plot
    plt.figure(figsize=(10, 6))

    plt.bar(r1, observed_yes, color='blue', width=bar_width, edgecolor='grey', label='Observed Yes')
    plt.bar(r2, expected_yes, color='cyan', width=bar_width, edgecolor='grey', label='Expected Yes')

    # Add labels
    plt.xlabel('Product', fontweight='bold')
    plt.xticks([r + bar_width / 2 for r in range(len(products))], products)
    plt.ylabel('Frequency', fontweight='bold')
    plt.title('Observed vs. Expected Frequencies (Yes Responses)', fontweight='bold')

    # Add legend
    plt.legend()

    # Show the plot
    plt.show()

def visualize_chi_square_results_yes_no():
    observed_yes = np.array([19, 3, 2, 2])
    observed_no = np.array([2, 0, 0, 0])

    # Total counts
    total_yes = np.sum(observed_yes)
    total_no = np.sum(observed_no)
    total = total_yes + total_no

    # Calculate expected frequencies
    expected_yes = (total_yes / total) * (observed_yes + observed_no)
    expected_no = (total_no / total) * (observed_yes + observed_no)

    # Create labels for products
    products = ['Mouse', 'Keyboard', 'Controller', 'Webcam']

    # Bar width
    bar_width = 0.35

    # Positions of the bars on the x-axis
    r1 = np.arange(len(products))
    r2 = [x + bar_width for x in r1]

    # Create the bar plot
    plt.figure(figsize=(10, 6))

    # plt.bar(r1, observed_yes, color='skyblue', width=bar_width, edgecolor='grey', label='Observed Yes')
    # plt.bar(r2, observed_no, color='tomato', width=bar_width, edgecolor='grey', label='Observed No')

    plt.bar(r1, expected_yes, color='cyan', width=bar_width, edgecolor='grey', alpha=0.5, label='Expected Yes',
            hatch='/')
    plt.bar(r2, expected_no, color='red', width=bar_width, edgecolor='grey', alpha=0.5, label='Expected No', hatch='/')

    # Add labels
    plt.xlabel('Product', fontweight='bold')
    plt.xticks([r + bar_width / 2 for r in range(len(products))], products)
    plt.ylabel('Frequency', fontweight='bold')
    plt.title('Observed vs. Expected Frequencies (Awareness Yes and No)', fontweight='bold')

    # Add legend
    plt.legend()

    # Show the plot
    plt.show()


if __name__ == '__main__':
    # perform_chi_square()
    visualize_chi_square_results_yes_no()