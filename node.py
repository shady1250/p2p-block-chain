from queue import Queue
from block import Block
import random

class Transaction:
    def __init__(self,transaction_str,timestamp,txn_id, from_id,to_id):   
        self.txn_id= txn_id
        self.transaction_str=transaction_str
        self.timestamp=timestamp
        self.first_time=0
        self.from_id=from_id
        self.to_id= to_id

class Node:
    def __init__(self,id,speed,cpu,hk):

        #Parameters used to initialize a node consisting of various data structures and variables
        self.id=id
        
        if speed==1:
            self.speed = "slow"
        else:
            self.speed = "fast"
        
        if cpu==1:
            self.cpu = "low"
        else:
            self.cpu = "high"

        self.hashing_power = hk

        self.transactions=[]

        self.tx_list=[]
        self.random_start=0

        self.transaction_queue=Queue()

        self.txn_in_block_chain=[]

        self.genesis_block=Block(self.id,None,"genesis",0)

        self.block_chain={}

        self.block_chain[self.genesis_block.blockID]=self.genesis_block
        
        self.longest_chain=self.genesis_block.blockID

        self.chain_depth=1

        self.block_queue=Queue()

        self.is_selfish = 0

        self.selfish_queue = Queue()

        self.balance = random.randint(100000,200000)

        self.needed_random = 0
        

    
        

