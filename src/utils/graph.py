import networkx as nx 
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import pandas as pd 
from .helpers import get_edge_list

def make_bipartite_graph(df:pd.DataFrame) -> nx.Graph:
    """Function to create a bipartite graph from a list of edges."""
    ## get the nodes 
    nodes_a = df.index.tolist()
    nodes_b = df.columns.tolist()
    ## get the edge list
    edge_list = get_edge_list(df, filter=True)
    ## create a graph 
    G = nx.Graph()
    ## add the nodes A 
    G.add_nodes_from(nodes_a, bipartite=0)
    ## add the nodes B 
    G.add_nodes_from(nodes_b, bipartite=1)
    ## add the edges from edge_list 
    G.add_edges_from(edge_list)
    
    ## Adjust the Position of the graph 
    # Separate by group
    left_set, right_set = bipartite.sets(G)
    pos = {}
    # Update position for node from each group
    pos.update((node, (1, index)) for index, node in enumerate(left_set))
    pos.update((node, (2, index)) for index, node in enumerate(right_set))

    ## for each connection, add the corresponding value from the dataframe
    for edge in G.edges():
        G[edge[0]][edge[1]]['weight'] = df.loc[edge[0], edge[1]]
    
    return G, pos

def show_graph(g:nx.Graph, pos:dict) -> None:
    """Shows the graph with the given position"""
    nx.draw(g, pos=pos)
    plt.show()