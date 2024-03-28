from networkproperties import Network
from generatetransactions import generate_transactions
from transmittransactions import transmit_transactions
import simpy
from graph import gen_graph
from checktransactionqueue import check_transactions_queue
from createblocks import create_blocks
from handleblocks import handle_blocks
import numpy as np

def generate_p_matrix(num_nodes):
    # Initialize an empty matrix for p_ij
    p_ij = np.zeros((num_nodes, num_nodes))
    # Generate random values for each element of p_ij
    for i in range(num_nodes):
        for j in range(num_nodes):
            p_ij[i][j] = np.random.uniform(0.01, 0.5)
    return p_ij

#number of peers
n=30

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

for node in peer_network.graph:
    id=node.longest_chain
    
    while id!=node.genesis_block.blockID:        
        print(node.block_chain[id].blockID)
        id=node.block_chain[node.block_chain[id].parent].blockID 
    
    print()
    print()

# for node in peer_network.graph:
#     print(node.chain_depth)
