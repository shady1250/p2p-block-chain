def transmit_transactions(env,node,peer_network, share_transaction_lock): 

    while True:
        neighbors=list(peer_network.graph.neighbors(node))

        l=[]  
        with share_transaction_lock.request() as req:
            yield req
            current=node.transactions
            for neighbor in neighbors:
                for c in current:
                    if c.txn_id not in node.tx_list:
                        neighbor.transaction_queue.put(c)
                        l.append(c.txn_id)

            l=list(set(l))
            for i in l:
                node.tx_list.append(i)      

        yield env.timeout(1)

    