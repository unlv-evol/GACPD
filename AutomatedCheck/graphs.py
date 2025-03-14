import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

"""
I never used networkx before so here are the links I used to learn how to set it up
Graph Creation: https://networkx.org/documentation/stable/tutorial.html#using-a-stochastic-graph-generator-e-g
Triangles: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cluster.triangles.html
(Also for triangles I asked for help on discord)
Diameter: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.distance_measures.diameter.html
Betweeness: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.betweenness_centrality.html


"""

n = [100]
d = [30, 20, 10]

for degree in d:
    for size in n:
        p = degree/size

        g1 = nx.erdos_renyi_graph(size, p)

        while nx.is_connected(g1) is False:
            g1 = nx.erdos_renyi_graph(size, p)

        nx.draw(g1)
        plt.show()

        print(f"======= For Degree: {degree}, Size: {size} =======")
        triangles = 0
        for key, value in nx.triangles(g1).items():
            triangles += value

        print(f"Triangles: {triangles//3}")

        diameter = nx.diameter(g1)
        print(f"Diameter: {diameter}")

        betweeness = nx.betweenness_centrality(g1)  # use of nodes * 1000 & Use between centrality for graphs
        sumVal = 0
        test = {}
        for key, value in betweeness.items():
            test[key] = value * 100000
            sumVal += value

        avg = sumVal/len(betweeness)
        print(f"Betweeness: {avg}")

        check = list(test.values())
        xVal, yVal = np.unique(check, return_counts=True)

        plt.xlabel("Degree Count")
        plt.ylabel("Vertice")
        plt.title("Degree Plot with a log-log showcase.")
        plt.scatter(xVal, yVal, color='red')
        plt.show()