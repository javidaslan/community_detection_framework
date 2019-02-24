from operator import add
from math import log2
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


def nmi_calculator(real_communities, found_communities):
    """
    Calculate Normalised Mutual Information
    """
    N_ij_s = generate_confusion_matrix(real_communities, found_communities)
    return calculate_numerator_of_formula(N_ij_s) / calculate_denominator_of_formula(N_ij_s)
    
def snmi(nmi, real_communities, found_communities):
    """
    Calculate Scaled NMI
    Ref:
    Alessia Amelio, Clara Pizzuti - Is Normalized Mutual Information a Fair Measure for Comparing Community Detection Methods? 
    2015 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining
    """
    power_of_exp = (len(real_communities) - len(found_communities))/len(real_communities)
    snmi = exp(-power_of_exp) * nmi
    return snmi