"""
Purity calculator
"""


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

def purity(n, X, Y):
    """
    Calculate purity
    """
    purity, purity_of_xi = 0, 0    
    for x_i in X:
        purity_of_xi += calculate_purity_of_xi(x_i, Y)
    
    return purity_of_xi/n
        
