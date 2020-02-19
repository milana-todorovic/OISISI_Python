from datetime import datetime

from searchengine.file_util.parser import Parser as HTMLFileParser
from searchengine.file_util import file_finder
from searchengine.data_structures.graph import Graph
from searchengine.data_structures.trie import Trie
from searchengine.data_structures.set import Set

class SearchEngine:
    """Klasa koja sadrzi strukture i parametre neophodne za pretragu."""

    def __init__(self):
        # TODO napravi prazne strukture i default parametre
        self.graph = Graph()
        self.trie = Trie()

    def loadroot(self, rootdir):
        # TODO dodavanje u trie

        htmlfiles = file_finder.findext(rootdir, ".html", ".htm")
        if len(htmlfiles) == 0:
            return False

        self.graph = Graph(htmlfiles)
        self.trie = Trie()

        htmlparser = HTMLFileParser()
        # bez ikakvih struktura podataka - 10 do 11 sekundi
        # sa grafom priblizno isto
        # paralalizacija? trie je problematican
        for file in htmlfiles:
            links, words = htmlparser.parse(file)
            self.graph.insert_edge(file, links)
            s = Set(map(str.lower, words))
            for word, val in s.elements.items():
                self.trie.add(word, file, val)

        return True


    def search(self, query):
        # TODO parsiraj i obradi upit
        pass

    # TODO dodati setere za parametre za rangiranje


if __name__ == "__main__":
    # TODO pokretati odavde? napraviti odvojen fajl za pokretanje? pokretati kao modul ili ne??
    start = datetime.now()
    se = SearchEngine()
    se.loadroot("C:\\Users\\Win 10\\Downloads\\python-2.7.7-docs-html")
    print(datetime.now() - start)
