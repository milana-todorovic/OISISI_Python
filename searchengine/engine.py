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



    def unos_upita(self):
        print(datetime.now() - start)
        upit = input("Unesite upit:")

        reci = upit.strip().split(" ")
        for i in range(len(reci)):
            reci[i]=reci[i].lower()

        print(reci)
        running=True
        while running:
            if not upit:
                print("\t Upit: " + upit)
                print("Pogresno je uneti prazan string.")
                upit,reci = ponovni_unos()
            elif (reci.count('and') + reci.count('or') + reci.count('not')) > 1:
                print("Imamo vise od jednog logickog operatora!")
                upit,reci = ponovni_unos()
            elif 'and' in reci:
                uspesno = True
                if len(reci)==3:
                        indeksAnd = reci.index('and')
                        if indeksAnd!=1:
                            print("Logicki operator AND moze samo da bude na poziciji 1!")
                            upit, reci = ponovni_unos()
                            uspesno = False
                        else:
                            #TODO izvrsiti pretragu na osnovu AND-a
                            pass

                else:
                    print("Logicki operator AND  moze da se pojavi samo izmedju 2 reci")
                    upit, reci = ponovni_unos()
                    uspesno = False

                if uspesno == True:
                    running=False
            elif 'or' in reci:
                uspesno = True
                if len(reci) == 3:
                        indeksOr = reci.index('or')
                        if indeksOr != 1:
                            print("Logicki operator OR moze samo da bude na poziciji 1!")
                            upit, reci = ponovni_unos()
                            uspesno = False
                        else:
                            # TODO izvrsiti pretragu na osnovu OR-a
                            pass

                else:
                    print("Logicki operator OR  moze da se pojavi samo izmedju 2 reci")
                    upit, reci = ponovni_unos()
                    uspesno = False

                if uspesno == True:
                    running = False

            elif 'not' in reci:
                uspesno = True
                if len(reci) == 3:
                        indeksNot = reci.index('not')
                        if indeksNot != 1:
                            print("Logicki operator NOT moze samo da bude na poziciji 1!")
                            upit, reci = ponovni_unos()
                            uspesno = False
                        else:
                            # TODO izvrsiti pretragu za NOT
                            pass

                else:
                    print("Logicki operator NOT  moze da se pojavi samo izmedju 2 reci")
                    upit, reci = ponovni_unos()
                    uspesno = False

                if uspesno == True:
                    running = False
            else:
                running=False



    def search(self, query):
        # TODO parsiraj i obradi upit
        pass

    # TODO dodati setere za parametre za rangiranje

def ponovni_unos():
    upit = input("Greska: Nepravilan unos, unesite ponovo ispravan upit:")
    reci = upit.strip().split(" ")
    for i in range(len(reci)):
        reci[i] = reci[i].lower()

    return upit,reci

if __name__ == "__main__":
    # TODO pokretati odavde? napraviti odvojen fajl za pokretanje? pokretati kao modul ili ne??
    start = datetime.now()
    se = SearchEngine()
    se.loadroot("C:\\Users\\Win 10\\Downloads\\python-2.7.7-docs-html")
    se.unos_upita()
