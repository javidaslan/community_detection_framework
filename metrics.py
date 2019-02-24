from operator import add
from math import log, log2, factorial
from math import exp


def list_compare(list1, list2):
    """
    Find common elements of lists
    """
    return len([elm for elm in list1 if elm in list2])


def generate_confusion_matrix(real_communities, found_communities):
    """
    Confusion matrix N:
        rows - 'real' communities
        columns - found communities
        N[ij] - number of nodes in real community i which also appears in found community j
    """
    N_ij_s = []
    for r_community in real_communities:
        n_ij = []
        for f_community in found_communities:
            n_ij.append(list_compare(r_community, f_community))
        N_ij_s.append(n_ij)

    return N_ij_s


def sum_over_per_row(N_ij_s):
    """
    Helper function to calculate the sum over row i in N[ij] confusion matrix N
    """
    return [sum(n_i) for n_i in N_ij_s]


def sum_over_per_column(N_ij_s):
    """
    Helper function to calculate the sum over column j in N[ij] confusion matrix N
    """
    sums = [0] * len(N_ij_s[0])
    for n_i in N_ij_s:
        sums = list(map(add, sums, n_i))
    
    return sums


def calculate_numerator_of_formula(N_ij_s):
    """
    For sake of simplicity denominator and numerator will be calculated in diferent methods
    """
    
    N_i = sum_over_per_row(N_ij_s)
    N_j = sum_over_per_column(N_ij_s)
    N_ij_sum = sum(N_i)
    s = 0
    for i in range(len(N_ij_s)):
        for j in range(len(N_ij_s[i])):
            result = (N_ij_s[i][j] * N_ij_sum) / (N_i[i] * N_j[j])
            if result != 0:
                s += N_ij_s[i][j] * log2( (N_ij_s[i][j] * N_ij_sum) / (N_i[i] * N_j[j]) )
    return -2 * s


def calculate_denominator_of_formula(N_ij_s):
    """
    For sake of simplicity denominator and numerator will be calculated in diferent methods
    """
    entropy_real_communities = 0
    entropy_found_communities = 0
    N_i = sum_over_per_row(N_ij_s)
    N_j = sum_over_per_column(N_ij_s)
    N_ij_sum = sum(N_i)

    for i in N_i:
        entropy_real_communities += i * log2(i/N_ij_sum)
    
    for j in N_j:
        entropy_found_communities += j * log2(j/N_ij_sum)
    
    return entropy_real_communities + entropy_found_communities


def calculate_nmi(real_communities, found_communities):
    """
    Calculate Normalised Mutual Information
    """
    N_ij_s = generate_confusion_matrix(real_communities, found_communities)
    return calculate_numerator_of_formula(N_ij_s) / calculate_denominator_of_formula(N_ij_s)
    

def calculate_snmi(nmi, real_communities, found_communities):
    """
    Calculate Scaled NMI
    Ref:
    Alessia Amelio, Clara Pizzuti - Is Normalized Mutual Information a Fair Measure for Comparing Community Detection Methods? 
    2015 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining
    """
    power_of_exp = (len(real_communities) - len(found_communities))/len(real_communities)
    snmi = exp(-power_of_exp) * nmi
    return snmi


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
    a_is = sum_over_per_row(contingency_matrix)
    b_js = sum_over_per_column(contingency_matrix)
    
    sum_a, sum_b = 0,0

    for a_i in a_is:
        sum_a += calculate_binomial_coefficient(a_i, 2)
    for b_j in b_js:
        sum_b += calculate_binomial_coefficient(b_j, 2)

    return sum_a, sum_b


def calculate_ari(n, x, y):
    """
    Calculate Adjusted Rand Index based on formula:
    https://wikimedia.org/api/rest_v1/media/math/render/svg/b1850490e5209123ab6e5b905495b4d5f9a1f661
    """
    contingency_matrix = generate_confusion_matrix(x, y)
    index = calculate_index(contingency_matrix)
    sum_a, sum_b = calculate_expectations(contingency_matrix)
    expected_index = (sum_a * sum_b)/calculate_binomial_coefficient(n, 2)
    max_index = (sum_a + sum_b)/2

    ari = (index - expected_index)/(max_index - expected_index)

    return ari


def calculate_purity_of_xi(x_i, Y):
    """
    The purity of a part x[i] relatively to the other partition Y
    """
    #find intersections
    intersections = []
    for y_j in Y:
        intersection = list(set(x_i) & set(y_j))
        intersections.append(len(intersection))
    return max(intersections)


def calculate_purity(n, X, Y):
    """
    Calculate purity
    """
    purity, purity_of_xi = 0, 0    
    for x_i in X:
        purity_of_xi += calculate_purity_of_xi(x_i, Y)
    
    return purity_of_xi/n


def calculate_f_measure(n, X, Y):
    """
    Calculate F - Measure
    """
    purity_x_y = calculate_purity(n, X, Y)
    purity_y_x = calculate_purity(n, Y, X)

    return (2*purity_x_y*purity_y_x)/(purity_x_y + purity_y_x)


def calculate_vi(X, Y):
  n = float(sum([len(x) for x in X]))
  sigma = 0.0
  for x in X:
    p = len(x) / n
    for y in Y:
      q = len(y) / n
      r = len(set(x) & set(y)) / n
      if r > 0.0:
        sigma += r * (log(r / p, 2) + log(r / q, 2))
  return abs(sigma)