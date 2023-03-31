import matplotlib.pyplot as plt
import networkx as nx

def printGraph(nodes):
    graph = nx.DiGraph() # On crée le graphe
    # On crée les arêtes
    for i in range(len(nodes) - 1):
        graph.add_node(nodes[i].getID())
        graph.add_edge(nodes[i].getPrev().getID(), nodes[i].getID())
        graph.add_edge(nodes[i].getID(), nodes[i].getNext().getID())
    # On affiche le graphe
    nx.draw(graph, with_labels=True)
    plt.show()