import random
from node import Transaction
import numpy as np

def print_stats(res):
    print(f'{res.count} of {res.capacity} slots are allocated.')
    print(f'  Users: {res.users}')
    print(f'  Queued events: {res.queue}')

txn=1
def generate_transactions(env,peer_network, node,n,resource):
    global txn
    while True:
        if txn>=1000:
             break

        # if(node.random_start==0):
        #     random_start = random.expovariate(1)  # Exponential distribution
        #     yield env.timeout(random_start) #start generation of transactions at a random time
        #     node.random_start=1

        while True:
                to_node=random.randint(1,n-1)  #transaction recieving node
                if to_node==node.id:
                    continue
                else:
                    break

        amount=random.randint(500,600)

        #print_stats(resource)
        with resource.request() as req:
            yield req         
            transaction = f"{txn}: {node.id} pays {to_node} {amount} coins at {node.id}"
            print(transaction)
            node.transactions.append(Transaction(transaction, env.now,txn, node.id, to_node))
            txn += 1


        # Wait for a random time before generating the next transaction
        rate_parameter = 1 / peer_network.tx
        next_txn = np.random.exponential(scale=1/rate_parameter, size=1)
        yield env.timeout(next_txn)

    
        