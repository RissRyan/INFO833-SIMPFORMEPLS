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

On fois que ce noeud est trouvé on appelle la méthode insertNode() qui permetra de casser l'ancienne liason et d'insérer le nouveau noeud entre les deux noeuds (le noeud trouvé et son noeud suivant original).

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

On utilise les méthodes sendMessage() et receiveMessages() de la classe Node.

Voici un exemple présent dans le fichier main.py : 

<p align="center"> 
<img src="img\messages.PNG" height=300>
</p>

Ici chaque noeud envoie un message au noeud suivant et attend un message de son noeud précédent.

Il y a aussi un message du noeud 4 au noeud 7 pour tester avec des chemins plus longs et un message du noeud 6 à lui-même.

## Etape 3 - Stockage de données

Pour le stockage des données et leurs extractions on procède comme ceci.

### La méthode put()

On crée d'abord une méthode findNodeForData() qui trouve un noeud ayant l'identifiant le plus proche de l'identifiant de la donnée.

Cette fonction ressemble énormément à la méthode join() à la différence qu'on autorise le fait que l'identifiant du noeud soit le même que celui de la donnée.

Ensuite une fois qu'on a trouvé le noeud auquel rattacher la donnée on envoie un message à ce noeud de la forme "PUT dataID replication".

Le noeud reçoit le message et le traite. Il enregistre le dataID et si la réplication > 0 il envoie le message à ses voisins proches en décrémentant la valeur de réplication.

Comme le demande l'énoncé la valeur de réplication vaut initialement 3.

### La méthode get()

On commence d'abord à savoir si on a la donnée.

Si ce n'est pas le cas alors on demande au prochain noeud si il a grâce à un message du type "GET dataID getterID" et ainsi de suite jusqu'à trouver un noeud ayant la donnée.

Si le noeud initial reçoit ce message alors on est sûr que la donnée n'existe pas.

Le fichier main.py a une fonction testData() permettant de tester ces méthodes.

## Etape 4 - Optimisation

On peut optimiser notre code en adoptant un point de vue général de l'anneau au lieu de faire du proche en proche.

En effet, on peut créer des méthodes prenant en paramètres l'ensemble des noeuds de l'anneau au lieu d'envoyer des requêtes de proche en proche.

Pour ce qui est du "piggybacking" j'ai l'impression d'avoir fait cela grâce à la méthode get() en donnant l'ID du getter.

## Les difficultés rencontrées

La principale difficulté rencontré a été simpy.

Premièrement pour le canal de discussion. J'ai pris beaucoup de temps à comprendre comment faire marcher simpy.Store().

Ensuite ça a été la gestion du temps. En effet, j'ai eu beaucoup de bugs lors de mes différentes simulations. J'ai pris un peu de temps à comprendre que cela était dû au faite que certains events se passaient avant d'autres.