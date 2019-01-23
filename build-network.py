import argparse
import logging
import pickle
from patient_record import *
from networkx import *
from itertools import combinations



def main():
    args = parse_args()
    logging.basicConfig(filename=args.log, level=logging.INFO)
    logging.info("begin script")

    providers_not_matched = set()

    dictionary_for_graph = {}

    at_risk_patients = set()
    with open("./computed-data/at-risk-patients.pickle", "r") as infile:
        at_risk_patients = pickle.load(infile)

    print "there are %i patients in this at risk object" % len(at_risk_patients)


    provider_subset = set()
    with open("./computed-data/subset-providers.pickle", "r") as infile:
        provider_subset = pickle.load(infile)
    print "there are %i providers n this subset: " % len(provider_subset)

    # now lets go back through original full data and build dict of provider: set(patientids)
    structured_dataset = []
    with open("./computed-data/structured-dataset.pickle", "r") as infile:
        structured_dataset = pickle.load(infile)

    for r in structured_dataset:
        # logging.info("now examing record: %s " % r)

        if r.PrescriberId in provider_subset:
            logging.info("prescriber %s is in our subset" % r.PrescriberId)

            logging.info("  adding patientid %s to prescriber key..." % r.PatientId)
            if dictionary_for_graph.has_key(r.PrescriberId):
                logging.info("      has key, adding %s to set..." % r.PatientId)
                dictionary_for_graph[r.PrescriberId].add(r.PatientId)
            else:
                logging.info("      key not found, creating new set with r.PatientId = %s " % r.PatientId)

                # warning: Don't do this:
                # dictionary_for_graph[r.PrescriberId] = set(r.PatientId)
                # set(r.PatientId) treats the ID string as an interable and breaks it up into single characters

                s = set()
                s.add(r.PatientId)
                dictionary_for_graph[r.PrescriberId] = s

            logging.info("set for providerid %s now looks like: %s " % (r.PrescriberId, dictionary_for_graph[r.PrescriberId]))
        else:
            providers_not_matched.add(r.PrescriberId)

    logging.info("finished with scanning data.")

    for k, v in dictionary_for_graph.iteritems():
        logging.info("key is %s and set is %s " % (k, v))

    logging.info("length of prescriber matches: %i " % len(dictionary_for_graph))
    logging.info("length of non-matches: %i " % len(providers_not_matched))

    g = nx.Graph()

    for k, v in dictionary_for_graph.iteritems():
        nodes = v
        edges = combinations(v, 2)

        #g.add_nodes_from(nodes)

        for n in nodes:
            at_risk = n in at_risk_patients
            #print "at risk for this node is %s " % at_risk
            g.add_node(n, at_risk=at_risk)

        g.add_edges_from(edges)


    # connected component might come in handy later
    # sub_graphs = nx.connected_component_subgraphs(g)


    print "number of nodes before pruning solitary: %i" % g.number_of_nodes()

    # Thank you to Dan Schult for the idea behind this pruning (updated method names)
    # https://groups.google.com/d/msg/networkx-discuss/XmP5wZhrDMI/tCPul0GI_LwJ
    solitary = [n for n, d in g.degree_iter() if d == 0]
    g.remove_nodes_from(solitary)

    print "number of nodes after pruning solitary: %i" % g.number_of_nodes()

    if is_connected(g):
        logging.info("graph is connected")
    else:
        logging.info("graph is not connected")
        cc = connected_component_subgraphs(g)
        #logging.info("there are %i subgraphs " % len(cc))

        subgraph_node_counts = []

        for sg in cc:
            # logging.info("this sg has %i nodes  " % sg.number_of_nodes())
            subgraph_node_counts.append(sg.number_of_nodes())

        subgraph_nodes_found = 0
        for c in subgraph_node_counts:
            subgraph_nodes_found = subgraph_nodes_found + c

        logging.info("found %i total subgraphs, with average node count of %f "
                     % (len(subgraph_node_counts), (float(subgraph_nodes_found) / len(subgraph_node_counts))))

        largest_cc = max(nx.connected_component_subgraphs(g), key=len)
        logging.info("getting largest connected component...")

    G = largest_cc

    logging.info("pickling graph object...")
    with open("./computed-data/final-graph.pickle", "w") as outfile:
        pickle.dump(G, outfile)
    logging.info("finished pickling graph object.")


    #print("radius: %d" % radius(G))
    #print("diameter: %d" % diameter(G))
    #print("eccentricity: %s" % eccentricity(G))
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



    logging.info("end of script")




def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--log', default='/dev/stderr', help='log file (default=stderr')
    parser.add_argument('--out', default='/dev/stdout', help='output. default=stdout')

    return parser.parse_args()


if __name__ == '__main__':
    main()