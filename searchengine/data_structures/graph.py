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

    # TODO metoda za breadth first prolaz za rangiranje