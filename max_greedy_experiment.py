import itertools
from community import community_louvain
import sys
import numpy
import datetime
import networkx as nx
import argparse
from networkx.algorithms.community import *

from BenchmarkGenerator import BenchmarkGenerator
from create_report import create_report
from graph_helper_tools import calc_metrics

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


def greedy_modularity(G):
    return [sorted(community) for community in greedy_modularity_communities(G)]

def main(realizations, nodes, gamma, beta, mu, min_degree, max_degree, min_community, max_community):
    """
    Generate number of LFR Benchmarks and carry out experiments
    """
    results = []
    print("Generating benchmarks")
    bg = BenchmarkGenerator(nodes=nodes, beta=beta, gamma=gamma, mu=mu, min_degree=min_degree, max_degree=max_degree, min_community=min_community, max_community=max_community)
    G_lfr = bg.generate_benchmarks(realizations)
    print("Benchmarks have been generated")
    for G in G_lfr:
        print('-'*23 + str(realizations) + '-'*23)
        gt_communities = bg.detect_ground_truth_communities(G)
        print("Running algorithm")
        greedy_modularity_comms = greedy_modularity(G)
        print("Number of Ground - Truth communities: {0}".format(len(gt_communities)))
        print("Number of communities found: {0}".format(len(greedy_modularity_comms)))
        nmi, ari, vi, purity = calc_metrics(5000, gt_communities, greedy_modularity_comms)
        results.append((nodes, len(G.edges()), bg.calc_degree(G), gamma, beta, mu, len(gt_communities), len(greedy_modularity_comms), nmi, ari, vi, purity))
        realizations -= 1
    print()
    create_report(results)


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
    