from searchengine.file_util.parser import Parser as HTMLFileParser
from searchengine.file_util import file_finder
from searchengine.data_structures.graph import Graph
from searchengine.data_structures.set import Set
from searchengine.data_structures.trie import Trie
import searchengine.core.ranking as ranking
from searchengine.query import simple_query
from searchengine.query.complex_query import ComplexQueryParser


class SearchEngine:
    """Klasa koja sadrzi strukture i parametre neophodne za pretragu."""

    def __init__(self):
        """Inicijalizuj prazne strukture za pretragu i podrazumevane parametre rangiranja."""
        self.graph = Graph()
        self.trie = Trie()
        self.rParams = ranking.RankingParameters()
        self.initLinkScores = {}
        self.complexParser = ComplexQueryParser()
        self.allPages = Set()

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
                self.trie.add(word, file, ranking.RankData(val, 1))

        self.initLinkScores = ranking.calculate_link_scores(self.graph, Set(htmlfiles), self.rParams.depth)

        # skup svih stranica, potreban za ! operator kod kompleksne pretrage
        self.allPages = Set()
        for page in htmlfiles:
            self.allPages.add(page, val=ranking.RankData(0, 1))

        return True

    def complex_search(self, query):
        """Pretrazi i rangiraj rezultat.

        Argumenti:
            query - kompleksni upit po kom se pretrazuje.
        """

        result = self.complexParser.parse(query).evaluate(self.trie, self.allPages)
        return ranking.rank_and_sort(self.graph, result, self.initLinkScores, self.rParams)

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

    def set_or_weight(self, orWeight):
        """Izmeni uticaj or upita na rangiranje.
        
        Argumenti:
            orWeight - vrednost izmedju 0 i 1. Za rezultat koji sadrzi N reci u or upitu,
            konacni rang se racuna po formuli rang*((N - 1) * orWeight + 1)
        """

        self.rParams.orWeight = orWeight

    def set_depth(self, depth):
        """Izmeni dubinu do koje se obilazi graf pri racunanju uticaja linkova na rang.

        Argumenti:
            depth - prirodan broj ili None. Velika vrednost ovog parametra znacajno
            degradira performanse pretrage.
        """
        self.rParams.depth = depth
        self.initLinkScores = ranking.calculate_link_scores(self.graph, Set(self.graph.get_nodes()), self.rParams.depth)

    def set_influences(self, wordInfluence, relLinkInfluence, genLinkInfluence):
        """Izmeni uticaj razlcitih komponenti na rang stranice. 

        Argumenti:
            Ocekuje se da je zbir argumenata 100.
            wordInfluence - uticaj reci, u procentima.
            relLinkInfluence - uticaj linkova sa stranica koje sadrze rec, u procentima.
            genLinkInfluence - uticaj linkova sa svih stranica, bez obrzira na broj reci, u procentima.
        """
        self.rParams.wordInf = wordInfluence
        self.rParams.relevantLinkInf = relLinkInfluence
        self.rParams.generalLinkInf = genLinkInfluence
