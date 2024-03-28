import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(G):

    pos = nx.spring_layout(G) 
    node_labels = {node: node.id for node in G.nodes()} 
    nx.draw(G, pos, with_labels=False, node_size=500, node_color='skyblue', edge_color='gray')  
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=12, font_color='black')  
    plt.savefig("graph")
    