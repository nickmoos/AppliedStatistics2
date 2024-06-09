import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import chi2
from scipy import stats


def perform_chi_square():
    observed_yes = np.array([19, 3, 2, 2])
    observed_no = np.array([2, 0, 0, 0])

    total_yes = np.sum(observed_yes)
    total_no = np.sum(observed_no)
    total = total_yes + total_no

    expected_yes = (total_yes / total) * (observed_yes + observed_no)
    expected_no = (total_no / total) * (observed_yes + observed_no)

    chi_square_yes = np.sum((observed_yes - expected_yes) ** 2 / expected_yes)
    chi_square_no = np.sum((observed_no - expected_no) ** 2 / expected_no)
    chi_square_total = chi_square_yes + chi_square_no

    df = (len(observed_yes) - 1) * 1

    p_value = 1 - chi2.cdf(chi_square_total, df)

    critical_value = chi2.ppf(0.95, df)

    print(
        f"Chi-Square Total: {chi_square_total}, Degrees of Freedom: {df}, P-Value: {p_value}, Critical Value: {critical_value}")


def null_hypothesis_satisfaction():
    satisfaction_scores = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 3, 3, 3, 1]

    mean_satisfaction = np.mean(satisfaction_scores)
    std_deviation = np.std(satisfaction_scores, ddof=1)  # ddof=1 to use sample standard deviation
    n = len(satisfaction_scores)

    h_0 = 4
    t_value = (mean_satisfaction - h_0) / (std_deviation / np.sqrt(n))
    # Degrees of freedom
    df = n - 1
    # Critical value for one-tailed test at 95% confidence level
    critical_value = stats.t.ppf(0.05, df)
    # P-value for the t-test
    p_value = stats.t.cdf(t_value, df)
    # Decision
    if t_value > critical_value and p_value > 0.05:
        print("Accept H0")
    else:
        print("Reject H0")

    print(f"Mean Satisfaction Score: {mean_satisfaction:.2f}")
    print(f"Standard Deviation: {std_deviation:.2f}")
    print(f"T-Value: {t_value:.2f}")
    print(f"Critical Value: {critical_value:.2f}")
    print(f"P-Value: {p_value:.3f}")


if __name__ == '__main__':
    perform_chi_square()
    null_hypothesis_satisfaction()
