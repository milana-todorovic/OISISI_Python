from searchengine.file_util.parser import Parser as HTMLFileParser
from searchengine.file_util import file_finder
from searchengine.data_structures.graph import Graph
from searchengine.data_structures.set import Set
from searchengine.data_structures.trie import Trie
import searchengine.core.ranking as ranking
from searchengine.query import simple_query


class SearchEngine:
    """Klasa koja sadrzi strukture i parametre neophodne za pretragu."""

    def __init__(self):
        """Inicijalizuj prazne strukture za pretragu i podrazumevane parametre rangiranja."""
        self.graph = Graph()
        self.trie = Trie()
        self.rParams = ranking.RankingParameters()
        self.initLinkScores = {}

    def loadroot(self, rootdir):
        """Pronadji html fajlove u zadatom direktorijumu i pripremi strukture za pretragu.

        Argumenti:
            rootdir - direktorijum u kom ce se vrsiti pretraga.
        """
        htmlfiles = file_finder.findext(rootdir, ".html", ".htm")
        if len(htmlfiles) == 0:
            return False

        self.graph = Graph(htmlfiles)
        self.trie = Trie()

        htmlparser = HTMLFileParser()
        for file in htmlfiles:
            links, words = htmlparser.parse(file)
            self.graph.insert_edge(file, links)
            s = Set(map(str.lower, words))
            for word, val in s.elements.items():
                self.trie.add(word, file, val)

        self.initLinkScores = ranking.calculate_link_scores(self.graph, Set(htmlfiles), self.rParams.depth, self.rParams.decay)

        return True

    def simple_search(self, query):
        """Pretrazi i rangiraj rezultat.

        Argumenti:
            query - osnovni upit po kom se pretrazuje.
        """

        reci, operator = simple_query.parse(query)

        skupovi = []
        for rec in reci:
            skupovi.append(self.trie.find(rec))

        rezultujuci_skup = Set()
        if operator == "and":
            rezultujuci_skup = skupovi[0] & skupovi[1]
        elif operator == "not":
            rezultujuci_skup = skupovi[0] - skupovi[1]
        else:
            for skup in skupovi:
                rezultujuci_skup = rezultujuci_skup | skup

        return ranking.rank_and_sort(self.graph, rezultujuci_skup, self.initLinkScores, self.rParams)


    # TODO dodati setere za parametre za rangiranje
