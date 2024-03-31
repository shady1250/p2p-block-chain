import random

def handle_blocks(env, peer_network , node,resource):

    while True:
        with resource.request() as req:
            yield req
            while node.block_queue.qsize() !=0:
                

                block_attach=node.block_queue.get()
                node.needed_random = random.randint(1,100)
                for bnode in peer_network.graph:
                    if bnode.id == block_attach.creator:
                        if bnode.chain_depth > node.chain_depth:
                            continue_prop = 1
                        else:
                            continue_prop=0

                if continue_prop:
                
                    id=node.longest_chain

                    while id!=node.genesis_block.blockID :

                        if id==block_attach.parent:
                            
                            node.block_chain[block_attach.blockID]=block_attach
                            node.block_chain[block_attach.blockID].attach="yes"
                            block_attach.attach="yes"
                            temp_depth=0

                            temp_id=block_attach.blockID                        
                            

                            while temp_id!=node.genesis_block.blockID:
                                #print(temp_id,node.genesis_block.blockID)
                                temp_depth+=1
                                temp_id=node.block_chain[node.block_chain[temp_id].parent].blockID 
                                #print(temp_id,node.genesis_block.blockID)
                            
                            if temp_depth >= node.chain_depth:
                                node.longest_chain=block_attach.blockID

                            is_fast=0

                            for node in peer_network.graph:
                                if node.id==block_attach.creator:
                                    if node.speed=="fast":
                                        is_fast=1
                                    break
                            
                            pij = peer_network.normal_dist[block_attach.creator][node.id]

                            if is_fast==1 and node.speed=="fast":
                                cij=100*1024*1024 #bps
                            else:
                                cij=5*1024*1024 

                            modm=1024*8

                            dij = 96*1024/cij

                            latency_bw_nodes = pij + modm/cij + dij

                            yield env.timeout(latency_bw_nodes)

                            break
            
                        else:

                            id=node.block_chain[node.block_chain[id].parent].blockID 
                    
                    if block_attach.attach=="no":
                        node.block_queue.put(block_attach)

                    if node.is_selfish == 1:
                        neighbors=list(peer_network.graph.neighbors(node))


                        if (node.selfish_queue.qsize() - peer_network.lvc > 2) or (node.selfish_queue.qsize() - peer_network.lvc == 1):
                            block = node.selfish_queue.get()
                            for neighbor in neighbors:
                                neighbor.block_queue.put(block)
                        
                        if node.selfish_queue.qsize() - peer_network.lvc == 2 :
                            while node.selfish_queue.qsize() > 0 :
                                block = node.selfish_queue.get()
                                for neighbor in neighbors:
                                    neighbor.block_queue.put(block)

                

        yield env.timeout(1)