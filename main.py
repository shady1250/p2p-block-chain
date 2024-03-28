from networkproperties import Network
from generatetransactions import generate_transactions
from transmittransactions import transmit_transactions
import simpy
from graph import gen_graph
from checktransactionqueue import check_transactions_queue
from createblocks import create_blocks
from handleblocks import handle_blocks
import numpy as np
import csv
import networkx as nx
import matplotlib.pyplot as plt

def generate_p_matrix(num_nodes):
    # Initialize an empty matrix for p_ij
    p_ij = np.zeros((num_nodes, num_nodes))
    # Generate random values for each element of p_ij
    for i in range(num_nodes):
        for j in range(num_nodes):
            p_ij[i][j] = np.random.uniform(0.01, 0.5)
    return p_ij

#number of peers
n=10

#percentage which determines slow or fast
z0=20

#percentage which determines low cpu or high cpu 
z1=80

#tx = for generating expomnential distribution time
tx=2

normal_dist=generate_p_matrix(n)

#assign network properties and create nodes
peer_network=Network(n,z0,z1,tx,normal_dist)

# Create a simulation environment
env = simpy.Environment()


resource = simpy.Resource(env, capacity=1)

#generate graph for the nodes with minimum 3 and maximum 6 connections
peer_network.graph=gen_graph(peer_network)

for node in peer_network.graph:
    if node.is_selfish==1:
        peer_network.selfish_nodes.append(node)


for node in peer_network.graph:
    env.process(generate_transactions(env, peer_network, node , peer_network.n , resource))


for node in peer_network.graph:
    env.process(transmit_transactions(env, node , peer_network,resource ))

for node in peer_network.graph:
    env.process(check_transactions_queue(env,peer_network, node , resource))


for node in peer_network.graph:
    env.process(create_blocks(env, node,peer_network, resource))

for node in peer_network.graph:
    env.process(handle_blocks(env , peer_network, node, resource))


#Run the simulation
env.run(until=1000)  # Run the simulation for 100 time units

# for node in peer_network.graph:
#     id=node.longest_chain
    
#     while id!=node.genesis_block.blockID:        
#         print(node.block_chain[id].blockID)
#         id=node.block_chain[node.block_chain[id].parent].blockID 
    
#     print()
#     print()

# for node in peer_network.graph:
#     print(node.chain_depth)
def read_csv_to_graph(csv_file):
    G = nx.Graph()
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for _ in range(2): 
            next(reader)
        for row in reader:
            G.add_edge(row[0], row[1])
    return G

def assign_unique_integers(hash_dict):
    hash_to_int = {}
    for hash_code in hash_dict.keys():
        if hash_code not in hash_to_int:
            hash_to_int[hash_code] = len(hash_to_int)  # Assign a unique integer value
    return hash_to_int

# Convert block dictionary to integer pairs
def convert_to_integer_pairs(block_dict, hash_to_int_mapping):
    integer_pairs = []
    for block_id, block in block_dict.items():
        source_int = hash_to_int_mapping[block_id]
        if block.parent is not None:
            target_int = hash_to_int_mapping[block.parent]
            integer_pairs.append((source_int, target_int))
    return integer_pairs


# Write integer pairs to CSV file
def write_to_csv(integer_pairs, csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['source', 'target'])  # Write header
        writer.writerows(integer_pairs)
            
i=0
for node in peer_network.graph:
    g=node.block_chain
    hash_to_int_mapping = assign_unique_integers(g)


    integer_pairs = convert_to_integer_pairs(g, hash_to_int_mapping)

    csv_file = 'graph_data'+str(i)+'.csv'
    write_to_csv(integer_pairs, csv_file)
    i=i+1
    print(f"CSV file '{csv_file}' has been created successfully.")
    graph=read_csv_to_graph(csv_file)
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(graph)  
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=800, edge_color='gray', linewidths=1, font_size=10)
    plt.title('Graph Visualization')
    graph_name='graph_visualization'+str(i)+'.png'
    plt.savefig(graph_name)
    print('graph_visualization'+str(i)+'.png created successfully')

    plt.close()
    
    
    


        
    