import nmi_calculator
from math import factorial


def calculate_binomial_coefficient(m, n):
    """
    Calculate binomial coefficient
    """
    if m >= n:
        return factorial(m)/(factorial(n) * factorial(m-n))
    
    return 0

def calculate_index(contingency_matrix):
    """
    Calculate index
    """
    index = 0
    for i in range(len(contingency_matrix)):
        for n_ij in contingency_matrix[i]:
            index += calculate_binomial_coefficient(n_ij, 2)
    return index


def calculate_expectations(contingency_matrix):
    """
    Calculate expected index
    """
    a_is = nmi_calculator.sum_over_per_row(contingency_matrix)
    b_js = nmi_calculator.sum_over_per_column(contingency_matrix)
    
    sum_a, sum_b = 0,0

    for a_i in a_is:
        sum_a += calculate_binomial_coefficient(a_i, 2)
    for b_j in b_js:
        sum_b += calculate_binomial_coefficient(b_j, 2)

    return sum_a, sum_b



def ari_calculator(n, x, y):
    """
    Calculate Adjusted Rand Index based on formula:
    https://wikimedia.org/api/rest_v1/media/math/render/svg/b1850490e5209123ab6e5b905495b4d5f9a1f661
    """
    contingency_matrix = nmi_calculator.generate_confusion_matrix(x, y)
    index = calculate_index(contingency_matrix)
    sum_a, sum_b = calculate_expectations(contingency_matrix)
    expected_index = (sum_a * sum_b)/calculate_binomial_coefficient(n, 2)
    max_index = (sum_a + sum_b)/2

    ari = (index - expected_index)/(max_index - expected_index)

    return ari
