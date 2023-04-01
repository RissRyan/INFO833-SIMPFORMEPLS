import simpy
import random

class Node:
    def __init__(self, env, pipe, id):
        self.env = env
        self.id = id
        self.pipe = pipe
        self.prevNode = self
        self.nextNode = self
        self.dataIDs = []

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
    
    def printDataIDs(self):
        print(self.dataIDs)

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
    def join(self, newNode):

        print(f'[{self.env.now}] - {newNode.id} cherche un noeud à s\'y attacher')
        iNode = self
        initNode = iNode
        loopEnded = False
        iNode = iNode.nextNode

        while iNode.id >= newNode.id or newNode.id >= iNode.nextNode.id:
            print(f'[{self.env.now}] - {newNode.id} veut à s\'attacher à {iNode.id}')
            if iNode == initNode:
                loopEnded = True
                print("Boucle bouclé")
            if iNode.id >= iNode.nextNode.id and loopEnded:
                break
            else:
                iNode = iNode.nextNode
        print(f'[{self.env.now}] - {newNode.id} a trouvé un noeud auquel s\'attacher : {iNode.id}')

        newNode.insertNode(iNode)

    # Pour s'insérer dans l'anneau
    def insertNode(self, previousNode):
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


    ### GESTION DES MESSAGES

    def sendMessage(self, destID, message):
        print(f'[{self.env.now}] - {self.id} envoie : {message} à {destID}')
        self.pipe.put((self.id, destID, message))
    
    def receiveMessages(self):
        while True:
            message = yield self.pipe.get()
            senderID, destID, messageContent = message
            print(f'[{self.env.now}] - {destID} a reçu :  {messageContent} de {senderID}')
            splittedMessage = messageContent.split()
            if(splittedMessage[0] == "PUT"):

                dataID = splittedMessage[1]
                repl = splittedMessage[2]
                if(dataID not in self.dataIDs):
                    self.dataIDs.append(dataID)
                if(int(repl) > 0):
                 newRepl = int(repl) - 1
                 self.sendMessage(self.prevNode.id, f'PUT {dataID} {str(newRepl)}')
                 self.sendMessage(self.nextNode.id, f'PUT {dataID} {str(newRepl)}')
            if(splittedMessage[0] == "GET"):
                dataID = splittedMessage[1]
                getterID = splittedMessage[2]
                if dataID in self.dataIDs:
                    self.sendMessage(getterID, f'J\'ai la donnée {dataID}')
                elif(int(getterID) == self.id):
                    self.sendMessage(getterID, f'la donnée {dataID} n\'existe pas')
                else:
                    self.sendMessage(self.nextNode.id, messageContent)



    ### GESTION DES DONNEES 

    def put(self, dataID):
        nodeForData = self.findNodeForData(dataID)
        self.sendMessage(nodeForData.getID(), f'PUT {dataID} 3')
    
    def get(self, dataID):
        if dataID in self.dataIDs:
           self.sendMessage(self.id, f'J\'ai la donnée {dataID}')
        else:
           self.sendMessage(self.nextNode.id, f'GET {dataID} {self.id}')
    
    def findNodeForData(self, dataID):

        #print(f'[{self.env.now}] - {self.id} cherche un noeud pour la donnée d\'identifiant {dataID}')
        iNode = self
        initNode = iNode
        loopEnded = False
        iNode = iNode.nextNode

        while iNode.id > dataID or dataID >= iNode.nextNode.id:
            if iNode == initNode:
                loopEnded = True
                #print("Boucle bouclé")
            if iNode.id >= iNode.nextNode.id and loopEnded:
                break
            else:
                iNode = iNode.nextNode
        #print(f'[{self.env.now}] - {self.id} a trouvé un noeud auquel attacher la donnée d\'identifiant {dataID} : {iNode.id}')
    
        return iNode