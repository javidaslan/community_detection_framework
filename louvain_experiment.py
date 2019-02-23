import itertools
from community import community_louvain
import sys
import numpy
import datetime
import networkx as nx
import argparse
import time


from BenchmarkGenerator import BenchmarkGenerator
from create_report import create_report
from graph_helper_tools import calc_metrics, avg


def get_communities_from_partition(partition):
    """
    Partition is a dictionary where each key indicates node and value indicates community
    """
    #print("\nExtracting ground-truth communities")
    communities = []
    found_communities = []
    for key, value in partition.items():
        community = []
        if value not in found_communities:
            for l_key, l_value in partition.items():
                if value == l_value:
                    community.append(l_key)
            found_communities.append(value)
            communities.append(community)

    return communities


def main(realizations, nodes, gamma, beta, mu, min_degree, max_degree, min_community, max_community):
    """
    Generate number of LFR Benchmarks and carry out experiments
    """
    results, metrics = [], [] 
    print("Generating benchmarks")
    bg = BenchmarkGenerator(nodes=nodes, beta=beta, gamma=gamma, mu=mu, min_degree=min_degree, max_degree=max_degree, min_community=min_community, max_community=max_community)
    G_lfr = bg.generate_benchmarks(realizations)
    print("Benchmarks have been generated")
    start_time = time.time()
    for G in G_lfr:
        print('-'*23 + str(realizations) + '-'*23)
        gt_communities = bg.detect_ground_truth_communities(G)
        print("Running algorithm")
        louvain_communities = get_communities_from_partition(community_louvain.best_partition(G))
        print("Number of Ground - Truth communities: {0}".format(len(gt_communities)))
        print("Number of Louvain communities: {0}".format(len(louvain_communities)))
        nmi, snmi, ari, vi, purity, f_measure = calc_metrics(nodes, gt_communities, louvain_communities)
        results.append((nodes, len(G.edges()), bg.calc_degree(G), gamma, beta, mu, len(gt_communities), len(louvain_communities), round(nmi, 3),  round(snmi, 3), round(ari, 3), round(vi, 3), round(purity, 3), round(f_measure, 3)))
        metrics.append((nmi, snmi, ari, vi, purity, f_measure))        
        realizations -= 1
    print()
    avg_metrics = avg(metrics)
    create_report(results, "Louvain algorithm", time.time() - start_time, nodes, mu, avg_metrics)


if __name__ == '__main__':
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
        main(args['realizations'], args['nodes'], args['gamma'], args['beta'], args['mu'], args['min_degree'], args['max_degree'], args['min_community'], args['max_community'])
    
    except Exception as ex:
        print(ex)
        print("Please provide number of realizations")
    