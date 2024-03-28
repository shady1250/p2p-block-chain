#ρij + |m|/cij + dij
def check_transactions_queue(env, peer_network, node , resource):
    while True:        
        
        with resource.request() as req:
            yield req
            
            if node.transaction_queue.qsize() !=0:
                tx = node.transaction_queue.get()
                is_present = any(obj.txn_id == tx.txn_id for obj in node.transactions)
                
                if is_present==False:
                    

                    pij = peer_network.normal_dist[tx.from_id][tx.to_id]
                    speed=0
                    for node in peer_network.graph:
                        if node.id==tx.from_id or node.id==tx.to_id :
                            if node.speed=="fast":
                                speed+=1
                    if speed==2:
                        cij=100*1024*1024 #bps
                    else:
                        cij=5*1024*1024

                    modm=1024*8

                    dij = 96*1024/cij

                    latency_bw_nodes = pij + modm/cij + dij

                    
                    yield env.timeout(latency_bw_nodes)

                    node.transactions.append(tx)
        yield env.timeout(1)
                
        
