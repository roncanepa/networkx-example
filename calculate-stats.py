from networkx import *
import pickle
import numpy as np
import pandas as pd
from scipy import stats
from algo import *
from centrality import *

with open("./computed-data/final-graph.pickle") as infile:
    g = pickle.load(infile)

G = g

#print("radius: %d" % radius(G))
#print("diameter: %d" % diameter(G))
# print("eccentricity: %s" % eccentricity(G))
#print("center: %s" % center(G))
#print("periphery: %s" % periphery(G))
#print("density: %s" % density(G))
# draw(G)

# this part was wrong before. Must use int not string if that's what I built graph with in first place
# print "degree of 222 is %s" % nx.degree(g, 222)
print "number of nodes: %i" % G.number_of_nodes()
print "number of edges: %i" % G.number_of_edges()
# print "neighbors of 222: %s " % g.neighbors(222)
# print "nodes: %s " % g.nodes()
# print "edges: %s " % g.edges()

at_risk_nodes = (n for n in G if G.node[n]['at_risk'] == 1)
at_risk_list = list (at_risk_nodes)

not_at_risk_nodes = (n for n in G if G.node[n]['at_risk'] == 0)
not_at_risk_list = list(not_at_risk_nodes)

print "#### clustering coeff"
cluster = Clustering("clustering_coeff")
cluster.run(G, at_risk_list, not_at_risk_list)


print "#### betweenness centrality"
b = BetweennessCentrality("betweenness", at_risk_list,not_at_risk_list)
b.run(G)

print "#### degree centrality"
d = DegreeCentrality("degree-centrality", at_risk_list,not_at_risk_list)
d.run(G)




print "done."