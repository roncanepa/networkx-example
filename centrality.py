import abc
import numpy as np
import networkx as nx
from networkx import *
import pandas as pd
from scipy import stats


class Centrality:
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, at_risk_nodes, non_risk_nodes):
        self.d = {}
        self.algo_name = name
        self.at_risk_nodes = at_risk_nodes
        self.non_risk_list = non_risk_nodes
        self.at_risk_values = []
        self.non_risk_values = []

    @abc.abstractmethod
    def do_algo(self, g):
        pass

    def run(self, g):
        print "beginning run() of %s " % self.algo_name
        self.do_algo(g)

        print "done with algo, now parsing results..."
        for k, v in self.d.iteritems():
            if k in self.at_risk_nodes:
                #print "adding value %s to at_risk " % v
                self.at_risk_values.append(v)
            else:
                #print "adding value %s to non_risk " % v
                self.non_risk_values.append(v)

        df_at_risk = pd.DataFrame({self.algo_name: self.at_risk_values})
        df_not_at_risk = pd.DataFrame({self.algo_name: self.non_risk_values})

        z_stat, p_val = stats.ranksums(df_at_risk[self.algo_name], df_not_at_risk[self.algo_name])

        print "pval of %s is %s " % (self.algo_name, p_val)


class BetweennessCentrality(Centrality):
    def do_algo(self, g):
        self.d = betweenness_centrality(g)


class DegreeCentrality(Centrality):
    def do_algo(self, g):
        self.d = degree_centrality(g)