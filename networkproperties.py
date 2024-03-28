import random 
from node import Node

class Network:
    def __init__(self,n,z0,z1,tx,normal_dist):

        self.n=n

        self.z0=z0

        self.z1=z1

        self.nodes_list=[]

        self.create_nodes()

        self.selfish = 2

        self.graph=None

        self.selfish_nodes=[]

        self.tx = tx

        self.lvc=0

        self.normal_dist = normal_dist

    def create_nodes(self):
        
        slow=int((self.z0/100)*self.n)
        fast=self.n-slow

        low=int((self.z1/100)*self.n)
        high=self.n-low

        for i in range(int(self.n)):
            speed = 0
            cpu = 0

            gen1=random.randint(1,2)
            gen2=random.randint(1,2)

            if gen1==1:
                if slow>0:
                    speed=1
                    slow-=1
                else:
                    speed=2
                    fast-=1
            else:
                if fast>0:
                    speed=2
                    fast-=1
                else:
                    speed=1
                    slow-=1

            if gen2==1:
                if low>0:
                    cpu=1
                    low-=1
                else:
                    cpu=2
                    high-=1
            else:
                if high>0:
                    cpu=2
                    high-=1
                else:
                    cpu=1
                    low-=1

            self.nodes_list.append(Node(i+1,speed,cpu))
