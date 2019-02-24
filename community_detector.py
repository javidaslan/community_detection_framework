import itertools
import sys
import numpy
import datetime
import networkx as nx
import argparse
import time


from BenchmarkGenerator import BenchmarkGenerator
from create_report import create_report
from graph_helper_tools import calc_metrics, avg
from algorithms import detect_communities


algorithms = ["Async Fluidc", "Fast greedy algorithm", "Louvain algorithm", "Walktrap"]

def main(algorithm, realizations, nodes, gamma, beta, mu, min_degree, max_degree, min_community, max_community):
    """
    Main gateway for community detection
    """
    #Generate number of LFR Benchmarks and carry out experiments
    results, metrics, next_realization = [], [], realizations
    print("Generating benchmarks")
    bg = BenchmarkGenerator(nodes=nodes, beta=beta, gamma=gamma, mu=mu, min_degree=min_degree, max_degree=max_degree, min_community=min_community, max_community=max_community)
    G_lfr = bg.generate_benchmarks(realizations)
    print("Benchmarks have been generated")
    start_time = time.time() #Track execution time of algorithm
    for G in G_lfr:
        print('-'*23 + str(next_realization) + '-'*23)
        gt_communities = bg.detect_ground_truth_communities(G)
        print("Running algorithm")
        detected_communities = detect_communities(algorithm, G, gt_communities) 
        print("Number of Ground - Truth communities: {0}".format(len(gt_communities)))
        print("Number of communities found by {0} algorithm: {1}".format(algorithms[algorithm], len(detected_communities)))
        # Calculate metrics
        nmi, snmi, ari, vi, purity, f_measure = calc_metrics(nodes, gt_communities, detected_communities)
        results.append((nodes, len(G.edges()), bg.calc_degree(G), gamma, beta, mu, len(gt_communities), len(detected_communities), round(nmi, 4), round(snmi, 3), round(ari, 4), round(vi, 4), round(purity, 4), round(f_measure, 3)))
        metrics.append((nmi, snmi, ari, vi, purity, f_measure))
        next_realization -= 1
    print()
    avg_metrics = avg(realizations, metrics)
    create_report(results, algorithms[algorithm], time.time() - start_time, nodes, mu, avg_metrics)


try:

    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--realizations", required=True, help="number of realizations", type=int)
    ap.add_argument("-n", "--nodes", required=True, help="number of nodes", type=int)
    ap.add_argument("-g", "--gamma", required=True, help="gamma (or tau1)", type=float)
    ap.add_argument("-b", "--beta", required=True, help="beta (or tau2)", type=float)
    ap.add_argument("-m", "--mu", required=True, help="Mixing parameter mu", type=float)
    ap.add_argument("-mind", "--min-degree", required=True, help="Minimum Degree", type=int)
    ap.add_argument("-maxd", "--max-degree", required=True, help="Maximum Degree", type=int)
    ap.add_argument("-minc", "--min-community", required=True, help="Minimum Community", type=int)
    ap.add_argument("-maxc", "--max-community", required=True, help="Maximum Community", type=int)
    args = vars(ap.parse_args())

    print("\nALGORITHMS:\n ")
    for index, algorithm in enumerate(algorithms):
        print("{index}. {algorithm}".format(index=index+1, algorithm=algorithm))

    selected_algorithm = int(input("\nPlease choose an algorithm that you want to apply (Insert number): "))
    print("\nSelected algorithm: {0}".format(algorithms[selected_algorithm-1]))

    main(selected_algorithm-1, args['realizations'], args['nodes'], args['gamma'], args['beta'], args['mu'], args['min_degree'], args['max_degree'], args['min_community'], args['max_community'])

except ValueError as ex:
    print("Please enter list number of algorithm")
    