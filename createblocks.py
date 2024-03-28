import random
from block import Block

def create_blocks(env, node, peer_network ,resource):
   while True:
      

      with resource.request() as req:
         yield req

         check_transaction_list=[]
   
         id=node.longest_chain

         
         while id!=node.genesis_block.blockID:

            check_transaction_list.extend(node.block_chain[id].transactions)
            id=node.block_chain[node.block_chain[id].parent].blockID 
               

         
         block_transactions = [transaction for transaction in node.transactions if transaction not in check_transaction_list]

  
         block_transactions_sample = random.sample(block_transactions, min(len(block_transactions), 20))

         if len(block_transactions_sample)!=0:

            block_txn=[]

            for i in block_transactions_sample:
               block_txn.append(i.transaction_str)
               
         
            new_block=Block(node.id,node.longest_chain,block_txn,env.now)

            node.longest_chain=new_block.blockID

            node.block_chain[new_block.blockID]=new_block

            node.block_chain[new_block.blockID].attach="yes"
            
            node.chain_depth+=1

            if node.is_selfish==0:
               if peer_network.lvc < node.chain_depth:
                  peer_network.lvc = node.chain_depth
               neighbors=list(peer_network.graph.neighbors(node))
               for neighbor in neighbors:
                  neighbor.block_queue.put(new_block)
            
            if node.is_selfish == 1:
               
               node.selfish_queue.put(new_block)

            

      yield env.timeout(10)