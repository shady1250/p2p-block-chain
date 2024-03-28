def handle_blocks(env, peer_network , node,resource):

    while True:
        with resource.request() as req:
            yield req
            while node.block_queue.qsize() !=0:
                block_attach=node.block_queue.get()
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

                        break
        
                    else:

                        id=node.block_chain[node.block_chain[id].parent].blockID 
                
                if block_attach.attach=="no":
                    node.block_queue.put(block_attach)

                if node.is_selfish == 1:
                    neighbors=list(peer_network.graph.neighbors(node))


                    if (node.selfish_queue.qsize() - peer_network.lvc > 2) or (node.selfish_queue.qsize() - peer_network.lvc == 1):
                        print("wooooooooooooooooooooo")
                        block = node.selfish_queue.get()
                        for neighbor in neighbors:
                            neighbor.block_queue.put(block)
                    
                    if node.selfish_queue.qsize() - peer_network.lvc == 2 :
                        print("wiiiiiiiiiiiiiiiiiiiii")
                        while node.selfish_queue.qsize() > 0 :
                            block = node.selfish_queue.get()
                            for neighbor in neighbors:
                                neighbor.block_queue.put(block)

                

        yield env.timeout(5)