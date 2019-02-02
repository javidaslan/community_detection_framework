import networkx as nx
from networkx.algorithms.community import LFR_benchmark_graph
import random
import matplotlib.pyplot as plt


class BenchmarkGenerator():
    """
    Class to generate 
    1. Girvan - Newman benchmark
    2. LFR Benchmark
    """


    def __init__(self, nodes, beta, gamma, mu, min_degree, max_degree, min_community, max_community):
        """
        Initialize BenchmarkGenerator with given parameters
        """
        self._nodes = nodes
        self._beta = beta
        self._gamma = gamma
        self._mu = mu
        self._min_degree = min_degree
        self._max_degree = max_degree
        self._min_community = min_community
        self._max_community = max_community

    def generate_gn_benchmark(self, zout) :
        """
        Create a graph of 128 vertices, 4 communities, like in
        Community Structure in  social and biological networks.
        Girvan newman, 2002. PNAS June, vol 99 n 12

        community is node modulo 4
        """

        pout = float(zout)/96.
        pin = (16.-pout*96.)/31.
        graph = nx.Graph()
        graph.add_nodes_from(range(128))
        for x in graph.nodes() :
            for y in graph.nodes() :
                if x < y :
                    val = random.random()
                    if x % 4 == y % 4 :
                        #nodes belong to the same community
                        if val < pin :
                            graph.add_edge(x, y)

                    else :
                        if val < pout :
                            graph.add_edge(x, y)
        return graph


    def calc_degree(self, G):
        """
        Calculate the avarage degree by summing all degrees
        """
        sum_of_degrees = sum([j for i, j in G.degree]) / len(G.degree)
        return round(sum_of_degrees, 4)


    def detect_ground_truth_communities(self, G):
        """
        Helper function to extract ground truth communities from LFR Benchmar
        """
        print("Detecting Ground - Truth communities")
        gt_communities = {frozenset(G.nodes[v]['community']) for v in G}
        return [list(fs) for fs in gt_communities]


    def generate_lfr_benchmark(self):
        """
        Generate LFR benchmark
        """
        G = LFR_benchmark_graph(self._nodes, tau1=self._gamma, tau2=self._beta, mu=self._mu, min_degree=self._min_degree, max_degree=self._max_degree, 
                                    min_community=self._min_community, max_community=self._max_community)
        G.name = "LFR Benchmark with {0} nodes".format(self._nodes)
        return G


    def generate_benchmarks(self, num, graphs = []):
        """
        Generate number of LFR Benchmarks
        """
        if num != 0:
            try:
                print("{0} graphs left".format(num), end='\r')
                graphs.append(self.generate_lfr_benchmark())
                return self.generate_benchmarks(num-1, graphs)
            except nx.exception.ExceededMaxIterations:
                return self.generate_benchmarks(num, graphs)
        else:
            return graphs