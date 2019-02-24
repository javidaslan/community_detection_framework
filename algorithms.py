import networkx as nx

from community import community_louvain
from networkx.algorithms.community.asyn_fluid import asyn_fluidc
from networkx.algorithms.community import greedy_modularity_communities



def detect_communitities(algorithm, G, gt_communities):
    """
    Calculate community
    """
    if algorithm == 0:
        return algorithm_asyn_fluidc(G, len(gt_communities))
    elif algorithm == 1:
        return fast_greedy_modularity(G)
    elif algorithm == 2:
        return louvain_method(G)

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

def algorithm_asyn_fluidc(G, gt_communities_count):
    """
    Async Fluidc community detection algorithm
    Parés F., Garcia-Gasulla D. et al. “Fluid Communities: A Competitive and Highly Scalable Community Detection Algorithm”.
    https://arxiv.org/pdf/1703.09307.pdf
    """
    communities = [list(community) for community in asyn_fluidc(G, gt_communities_count, max_iter=100, seed=None)]

    return communities

def fast_greedy_modularity(G):
    """
    Fast greedy community detection algorithm
    Clauset, A., Newman, M. E., & Moore, C. “Finding community structure in very large networks.” Physical Review E 70(6), 2004.
    """
    return [sorted(community) for community in greedy_modularity_communities(G)]

def louvain_method(G):
    """
    """
    return get_communities_from_partition(community_louvain.best_partition(G))