import networkx as nx
import random

def gen_graph(peer_netwok):

    node_objects = peer_netwok.nodes_list
    # Create an undirected graph with minimum degree 3 and maximum degree 6 with nodes as node objects
    graph = nx.Graph()
    graph.add_nodes_from(node_objects)
    for i, node in enumerate(node_objects):
        current_degree = graph.degree(node)

        while current_degree < 3:
            remaining_nodes = set(node_objects) - set(graph.neighbors(node))
            if remaining_nodes:
                random_node = random.choice(list(remaining_nodes))
                if random_node != node:
                    graph.add_edge(node, random_node)
                    current_degree += 1
            else:
                break  

        while current_degree > 6:
            neighbor = random.choice(list(graph.neighbors(node)))
            graph.remove_edge(node, neighbor)
            current_degree -= 1

    while peer_netwok.selfish > 0:
        choose=random.randint(0,peer_netwok.n-1)
        for node in graph:
            if node.id == choose and node.is_selfish==0:
                node.is_selfish = 1
                peer_netwok.selfish -= 1



    return graph