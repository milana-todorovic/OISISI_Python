from collections import deque
import itertools

from searchengine.data_structures.set import Set


class Graph:
    """Implementacija usmerenog grafa zasnovana na upotrebi tipova dictionary i Set."""

    def __init__(self, nodes=[]):
        """Inicijalizuj graf.

        Argumenti:
            nodes - inicijalni cvorovi grafa. Ako se izostavi, kostruise se prazan
            graf.
        """
        self.edges = {}
        for node in nodes:
            self.edges[node] = Set()

    def insert_node(self, node):
        """Dodaj cvor u graf.

        Argumenti:
            node - cvor koji se dodaje.

        Ako prosledjeni cvor vec postoji u grafu, nista se ne desava.
        """
        if node not in self.edges:
            self.edges[node] = Set()

    def insert_edge(self, source, targets=[]):
        """Dodaj granu u graf.

        Argumenti:
            source - cvor kome je grana izlazna.
            targets - cvorovi kojima je grana ulazna.
        """
        if source not in self.edges:
            return

        for target in targets:
            if target in self.edges:
                self.edges[source].add(target)

    def get_nodes(self):
        """Vrati listu svih cvorova grafa."""
        return list(self.edges.keys())

    def get_edges(self):
        """Vrati dictionary sa granama grafa."""
        return self.edges

    def bfs(self, startNode, depth=None):
        """Vrati iterator za depth first obilazak grafa.
        
        Argumenti:
            startNode - cvor od kog pocinje obilazak.
            depth - dubina do koje treba obilaziti graf. None ako treba obici 
            citav graf.
        """
        queue = deque()
        obradjeni = set()

        if startNode in self.edges:
            queue.append((startNode, 1, 0))

        while len(queue) != 0:
            node, lnum, currdepth = queue.popleft()
            if (depth is None or currdepth < depth) and node not in obradjeni:
                link_num = len(self.edges[node])
                queue.extend(zip(self.edges[node], itertools.repeat(link_num * lnum), itertools.repeat(currdepth + 1)))
                obradjeni.add(node)
            yield node, lnum, currdepth
            

        