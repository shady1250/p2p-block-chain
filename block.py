import hashlib
class Block:
    def __init__(self,creator,parent,transactions,create_time_stamp):

        #It creates the block class with different parameters
        self.creator=creator
        self.transactions=transactions
        self.parent=parent
        self.blockID=self.createID()
        self.attach="no"
        self.create_time_stamp = create_time_stamp
        
        
        
    def createID(self):

        #USed to create the blockID using hashlib
        transactionString=""
        for txn in self.transactions:
            transactionString+=txn
        sha=hashlib.sha256(transactionString.encode())
        return sha.hexdigest()
    