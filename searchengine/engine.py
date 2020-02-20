from datetime import datetime
import random

from searchengine.file_util.parser import Parser as HTMLFileParser
from searchengine.file_util import file_finder
from searchengine.data_structures.graph import Graph
from searchengine.data_structures.set import Set
import searchengine.ranking as ranking

class SearchEngine:
    """Klasa koja sadrzi strukture i parametre neophodne za pretragu."""

    def __init__(self):
        # TODO napravi prazne strukture i default parametre
        self.graph = Graph()

    def loadroot(self, rootdir):
        # TODO dodavanje u trie

        htmlfiles = file_finder.findext(rootdir, ".html", ".htm")
        if len(htmlfiles) == 0:
            return False

        self.graph = Graph(htmlfiles)

        htmlparser = HTMLFileParser()
        # bez ikakvih struktura podataka - 10 do 11 sekundi
        # sa grafom priblizno isto
        # paralalizacija? trie je problematican
        for file in htmlfiles:
            links, words = htmlparser.parse(file)
            self.graph.insert_edge(file, links)

        return True

    def search(self, query):
        # TODO parsiraj i obradi upit
        pass

    # TODO dodati setere za parametre za rangiranje


if __name__ == "__main__":
    # TODO pokretati odavde? napraviti odvojen fajl za pokretanje? pokretati kao modul ili ne??
    start = datetime.now()
    se = SearchEngine()
    se.loadroot("C:\\Users\\Lana\\Desktop\\py\\test-skup")
    print(datetime.now() - start)
    s = Set()
    s1 = Set()
    for node in se.graph.get_nodes():
        s1.add(node, 1)
        s.add(node, random.randint(1, 200))
    r = ranking.RankingParameters()
    initLinkScores = ranking.calculate_link_scores(se.graph, s1, r.depth, r.decay)
    start = datetime.now()
    blah = ranking.rank_and_sort(se.graph, s, initLinkScores, r)
    print(datetime.now() - start)

    
    
    
