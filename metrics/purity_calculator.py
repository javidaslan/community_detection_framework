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

def f_measure(n, X, Y):
    """
    Calculate F - Measure
    """
    purity_x_y = purity(n, X, Y)
    purity_y_x = purity(n, Y, X)

    return (2*purity_x_y*purity_y_x)/(purity_x_y + purity_y_x)
        
