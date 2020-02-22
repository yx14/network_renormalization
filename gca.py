#import pkgs
import time
import networkx as nx
import numpy as np
import pickle as pkl
#import matplotlib.pyplot as plt

#inputs: N - the maximum number of nodes
#        m - mdeg(v) nodes get added to each node in the old graph 
#        e - probability of choosing an edge in the old graph vs an edge in the new graph
def fm(N, m, e):
    G = nx.Graph()
    G.add_edges_from([(0, i) for i in range(1, 5)]) #create a star graph
    while len(G.nodes) + 2*m*len(G.edges) < N:
        E_old = list(G.edges)
        index = len(G.nodes) #starting new node index 
        new_neighbors_dict = {} #track new neighbors for each v in old V
        for v in list(G.nodes).copy():
            edge_ct = m*len(list(G.neighbors(v)))
            new_neighbors_dict[v] = [i+index for i in range(edge_ct)]
            G.add_edges_from([(v, neighbor) for neighbor in new_neighbors_dict[v]])
            index += edge_ct
        for edge in E_old:
            if np.random.rand() < 1 - e: 
                G.remove_edge(*edge) #remove old edge
                #add new edge between nonhubs
                new_edge = (np.random.choice(new_neighbors_dict[edge[0]]),
                           np.random.choice(new_neighbors_dict[edge[1]]))
                G.add_edge(*new_edge)
    return G

#inputs: G - a graph
#        l_B - box size l_B
#output: newG - the transformed graph
def gca(G, l_B):
    #calculate distances between every vertex in G
    p = dict(nx.all_pairs_shortest_path_length(G, l_B))
    #add infs to p 
    for i in G.nodes:
        for j in set(G.nodes).difference(set(p[i].keys())):
            p[i][j] = np.inf
    #construct G' 
    Gp = nx.Graph()
    Gp.add_nodes_from(G.nodes)
    Gp.add_edges_from([(i, j) for i in G.nodes for j in p[i].keys() if p[i][j] > l_B])
    c = nx.greedy_color(Gp)
    '''
    #relabel the nodes 
    #node_order = np.random.permutation(Gp.nodes)
    #order_dict = {i:j for i, j in zip(Gp.nodes, node_order)}
    #Gp = nx.relabel_nodes(Gp, order_dict)
    
    #construct neighbor dict for Gp
    #Gp_neighbor_dict = {i:list(Gp.neighbors(i)) for i in Gp.nodes} #i:[] for lone nodes
    
  
    c = {} #coloring dictionary of node:color
    c[0] = 0 #default 
    for i in range(1, len(Gp.nodes)):
        possible_colors = set(range(i + 1))
        excluded_colors = set([c[j] for j in set(range(i)).intersection(Gp_neighbor_dict[i])])
        c[i] = min(possible_colors.difference(excluded_colors))  
    create the transformed graph
    '''
    newG = nx.Graph()
    #add nodes 
    new_nodes = list(set(c.values()))
    newG.add_nodes_from(new_nodes)
    #add edges 
    #get inv_c, color:[nodes]
    inv_c = {i:[j for j in Gp.nodes if c[j] == i] for i in c.values()}
    #get inv_neigh, color:[neighbors of nodes with this color IN G NOT IN Gp]
    #construct neighbor dict for G
    G_neighbor_dict = {i:list(G.neighbors(i)) for i in G.nodes}
    inv_neigh = {i: [l 
                     for k in [list(G_neighbor_dict[j]) for j in inv_c[i]]
                         for l in k] 
                     for i in c.values()}
    for i in new_nodes:
        #get nodes in 
        for j in set(new_nodes).difference(set([i])):
            for k in inv_c[i]:
                if k in inv_neigh[j]:
                    newG.add_edge(i, j)
                    break
    return newG

# calculate kappa 
def get_kappa(G):
    #find max degree 
    return max(dict(G.degree).values())/(len(G.nodes) - 1) 

#calculate x, the relative network size
def get_x(G, n_0):
    return len(G.nodes)/n_0
# calculate chi 
def get_chi(kappas):
    return (np.std(kappas))**2

# power-law fitting -> get from Ising lab 
#TO DO 
# saving 
# TO DO 

num_graphs = 10
for n in [20000]:
    n_0 = n #number of nodes in starting graph
    avg_deg = 2 #average degree of a node in the graph 
    l_B = 3 #max distance between nodes in a box 
    p = avg_deg/n_0 #probability of generating an edge between two nodes 
    kappas_all = [] #list of kappas=[] for all graphs 
    xs_all = []
    t = time.time()
    for i in range(num_graphs):
        test = nx.erdos_renyi_graph(n_0, p) #graph generation
        #perform GCA repeatedly and store the kappas 
        kappas = []
        xs = []
        while list(test.edges) != []:
            kappas.append(get_kappa(test))
            xs.append(get_x(test, n_0))
            test = gca(test, l_B)
        kappas_all.append(kappas)
        xs_all.append(xs)
        print(i, time.time() - t)
    print(n, time.time() - t)
    #10 graphs took 882 seconds 
    #get_kappa(test)
    #pickle data 
    filename = 'er' + str(n_0)
    f = open(filename,'wb')
    for i in [kappas_all, xs_all]:
        pkl.dump(i,f)
    f.close()
 
#B-A 
num_graphs = 10
for n in [20000]:
    n_0 = n #number of nodes in starting graph
    new_edges = 2 #number of edges to attach from a new node to existing nodes
    l_B = 3 #max distance between nodes in a box 
    kappas_all = [] #list of kappas=[] for all graphs 
    xs_all = []
    t = time.time()
    for i in range(num_graphs):
        test = nx.barabasi_albert_graph(n_0, new_edges, i) #graph generation
        #perform GCA repeatedly and store the kappas 
        kappas = []
        xs = []
        while list(test.edges) != []:
            kappas.append(get_kappa(test))
            xs.append(get_x(test, n_0))
            test = gca(test, l_B)
        kappas_all.append(kappas)
        xs_all.append(xs)
        print(i)
    print(time.time() - t)
    #10 graphs took 882 seconds 
    #get_kappa(test)
    #pickle data 
    filename = 'ba' + str(n_0)
    f = open(filename,'wb')
    for i in [kappas_all, xs_all]:
        pkl.dump(i,f)
    f.close()

 #fm
num_graphs = 10
for n in [20000]:
    n_0 = n #number of nodes in starting graph
    new_edges = 2 #number of edges to attach from a new node to existing nodes
    l_B = 3 #max distance between nodes in a box 
    kappas_all = [] #list of kappas=[] for all graphs 
    xs_all = []
    t = time.time()
    for i in range(num_graphs):
        test = fm(n_0, 2, 0.5) #graph generation
        #perform GCA repeatedly and store the kappas 
        kappas = []
        xs = []
        while list(test.edges) != []:
            kappas.append(get_kappa(test))
            xs.append(get_x(test, n_0))
            test = gca(test, l_B)
        kappas_all.append(kappas)
        xs_all.append(xs)
        print(i)
    print(time.time() - t)
    #10 graphs took 882 seconds 
    #get_kappa(test)
    #pickle data 
    filename = 'fm' + str(n_0)
    f = open(filename,'wb')
    for i in [kappas_all, xs_all]:
        pkl.dump(i,f)
    f.close()

