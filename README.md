# INFO833-DHT_SIMPY

## Le projet

Projet d'un système de réseau distribué. Le réseau est modélisé par un ensemble de noeuds donc la structure est en anneau.

Les noeuds seront capables de recevoir et d'envoyer des messages aux autres noeuds et de stocker les messages reçus.

On va utiliser Python, la librairie Simpy, Matplotlib et NetworkX pour implémenter et visualiser ce réseau.

## Etape 1 - Mise en place du réseau

On doit d'avoir implémenter le système de noeud et l'ajout et le retrait de ces noeuds.

On crée une classe Node qui modélisera chaque noeud.

Les attributs sont l'ID du noeud, l'environement et le pipe simpy et enfin le noeud précédent et suivant (je rapelle qu'on a une structure d'anneau).

En méthode il y a bien sûr le constructeur et les setters/getters mais aussi les méthodes join() et leave() qui permettent d'ajouter ou de retirer un noeud de l'anneau.

La méthode join() cherche un noeud dans l'anneau auquel rattacher le nouveau noeud. Le trouvé sera le noeud précedent du nouveau noeud.

On fois que ce noeud est trouvé on appelle la méthode insert() qui permetra de casser l'ancienne liason et d'insérer le nouveau noeud entre les deux noeuds (le noeud trouvé et son noeud suivant original).

La méthode leave() permet de retirer un noeud de l'anneau et de faire en sorte que ces noeuds voisins deviennent en relation pour le pas casser la boucle.

Le fichier main.py détaille l'utilisation de ces méthodes et permet d'afficher les graphes des différentes évolutions de l'anneau.

### Anneau de base : noeuds avec IDs 1, 4 et 7

<p align="center"> 
<img src="img\loop1.PNG" height=300>
</p>

### Ajout du noeud 6 

<p align="center"> 
<img src="img\loop2.PNG" height=300>
</p>

### On retire le noeud 1 

<p align="center"> 
<img src="img\loop3.PNG" height=300>
</p>

## Etape 2 - Envoie et réception de messages

C'est pour la gestion des messages qu'on commence à utiliser simpy.

En effet, simpy permet la gestion "facile" d'events. La réception et l'envoie de messages peuvent être considérés comme des events.

Il y a aussi l'utilisation d'un pipe qui fait office de cannal de discussion.

Voici un exemple présent dans le fichier main.py : 

<p align="center"> 
<img src="img\messages.PNG" height=300>
</p>

Ici chaque noeud envoie un message au noeud suivant et attend un message de son noeud précédent.
