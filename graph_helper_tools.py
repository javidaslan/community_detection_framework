from metrics import calculate_nmi, calculate_snmi, calculate_ari, calculate_vi, calculate_purity, calculate_f_measure

def calc_metrics(nodes, real_communities, detected_communities):
    """
    Calculate:

        1. Normalized Mutual Information
        2. Adjusted Rand Index
        3. Variation of Information
        4. Purity
    """
    print("Calculating metrics")
    nmi = calculate_nmi(real_communities, detected_communities)
    snmi = calculate_snmi(nmi, real_communities, detected_communities)
    ari = calculate_ari(nodes, real_communities, detected_communities)
    vi = calculate_vi(real_communities, detected_communities)
    purity = calculate_purity(nodes, real_communities, detected_communities)
    f_measure = calculate_f_measure(nodes, real_communities, detected_communities)
    print("NMI: {0}, SNMI: {1}, ARI: {2}, VI: {3}, Purity: {4}, F-Measure: {5}".format(round(nmi, 3), 
            round(snmi, 3), round(ari, 3),
            round(vi, 3), round(purity, 3), round(f_measure, 3)))
    return nmi, snmi, ari, vi, purity, f_measure

def avg(realizations, results):
    """
    Calculate average values of metrics 
    """
    avg_nmi, avg_snmi, avg_ari, avg_vi, avg_purity, avg_fmeasure = 0,0,0,0,0,0
    for nmi, snmi, ari, vi, purity, f_measure in results:
        avg_nmi += nmi
        avg_snmi += snmi
        avg_purity += purity
        avg_fmeasure += f_measure
        avg_vi += vi
        avg_ari += ari

    return round(avg_nmi/realizations, 3), round(avg_snmi/realizations, 3), round(avg_ari/realizations, 3), round(avg_vi/realizations, 3), round(avg_purity/realizations, 3), round(avg_fmeasure/realizations, 3)


    
    
