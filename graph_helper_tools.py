import nmi_calculator
import ari_calculator
import vi_calculator
import purity_calculator

def calc_metrics(nodes, real_communities, detected_communities):
    """
    Calculate:

        1. Normalized Mutual Information
        2. Adjusted Rand Index
        3. Variation of Information
        4. Purity
    """
    print("Calculating metrics")
    nmi = nmi_calculator.nmi_calculator(real_communities, detected_communities)
    ari = ari_calculator.ari_calculator(nodes, real_communities, detected_communities)
    vi = vi_calculator.variation_of_information(real_communities, detected_communities)
    purity = purity_calculator.purity(5000, real_communities, detected_communities)

    return nmi, ari, vi, purity