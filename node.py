import simpy
import random

class Node:
    def __init__(self, env, pipe, id):
        self.env = env
        self.id = id
        self.pipe = pipe
        self.prevNode = self
        self.nextNode = self

    ### SETTERS ET GETTERS

    def getID(self):
        return self.id
    
    def getPrev(self):
        return self.prevNode
    
    def setPrev(self, prev):
        self.prevNode = prev
    
    def getNext(self):
        return self.nextNode
    
    def setNext(self, next):
        self.nextNode = next

    # Fonction obsolète, on utilise l'affiche de graphe qui est plus adéquat
    def printNode(self):

        print("ID : " + str(self.id))

        if(self.prevNode != None):
            print("PREV : " + str(self.prevNode.getID()))
        else:
            print("PREV : " + str(self.prevNode))
        if(self.nextNode != None):
            print("NEXT : " + str(self.nextNode.getID()))      
        else:
            print("NEXT : " + str(self.nextNode))

    # Pour rejoindre l'anneau
    def join(self, ring):

        print(f'[{self.env.now}] - {self.id} cherche un noeud à s\'y attacher')
        iNode = ring[random.randint(0, len(ring) - 1)] 
        initNode = iNode
        loopEnded = False
        iNode = iNode.nextNode

        while iNode.id >= self.id or self.id >= iNode.nextNode.id:
            print(f'[{self.env.now}] - {self.id} veut à s\'attacher à {iNode.id}')
            if iNode == initNode:
                loopEnded = True
                print("lap_complete")
            if iNode.id >= iNode.nextNode.id and loopEnded:
                break
            else:
                iNode = iNode.nextNode
        print(f'[{self.env.now}] - {self.id} a trouvé un noeud auquel s\'attacher : {iNode.id}')
        
        ring.append(self)
        self.insert(iNode)

    # Pour s'insérer dans l'anneau
    def insert(self, previousNode):
        self.prevNode = previousNode
        self.nextNode = previousNode.getNext()
        previousNextNode = previousNode.getNext()
        previousNextNode.setPrev(self)
        previousNode.setNext(self)

    # On quite l'anneau
    def leave(self, ring):
        self.prevNode.nextNode = self.nextNode
        self.nextNode.prevNode = self.prevNode
        ring.remove(self)

    def sendMessage(self, destID, message):
        print(f'[{self.env.now}] - {self.id} envoie : {message} à {destID}')
        self.pipe.put((destID, message))
    
    def receiveMessages(self):
        while True:
            message = yield self.pipe.get()
            yield self.env.timeout(random.randint(1, 2))
            senderID, messageContent = message
            print(f'[{self.env.now}] - {self.id} a reçu :  {messageContent} de {senderID}')
