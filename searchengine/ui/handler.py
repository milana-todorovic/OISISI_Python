from datetime import datetime

from searchengine.core.engine import SearchEngine
from searchengine.query.simple_query import SimpleQueryError
from searchengine.ui.pagination import Pagination


class UIHandler:
    """Klasa koja sadrzi metode za interakciju sa korisnikom."""

    def __init__(self):
        """Inicijalizuj strukture za pretragu i izaberi direktorijum."""

        self.engine = SearchEngine()
        self.resultsPerPage = 10
        self.choose_root()

    def main_menu(self):
        """Prikazi glavni meni."""

        running = True
        while running:
            print()
            print("S - Osnovna pretraga")
            print("C - Promena direktorijuma za pretragu")
            print("O - Ostale postavke")
            print("Bilo koji drugi karakter za završetak rada.")
            op = input("\t>> ").lower()
            if op == "s":
                self.simple_search()
            elif op == "c":
                self.choose_root()
            elif op == "o":
                self.settings()
            else:
                running = False

    def choose_root(self):
        """Izaberi direktorijum za pretragu."""

        wrong = True
        while wrong:
            print()
            rootdir = input("Unesite željeni direktorijum.\n\t>> ")
            print("Učitavanje...")
            start = datetime.now()
            if self.engine.loadroot(rootdir):
                print("Učitavanje uspešno. Utrošeno vreme: " + str(datetime.now() - start))
                wrong = False
            else:
                print("Unesena putanja nije postojeći direktorijum ili ne sadrži html fajlove!")

    def simple_search(self):
        """Pretrazi po osnovnom upitu."""

        search = True
        while search:
            print()
            query = input("Unesite upit (enter za povratak na glavni meni).\n\t>> ")
            if query == "":
                search = False
            else:
                try:
                    start = datetime.now()
                    res = self.engine.simple_search(query)
                    print("Utrošeno vreme: " + str(datetime.now() - start))
                    search = self.show_search_result(res)
                except SimpleQueryError as err:
                    print(err.message)

    def show_search_result(self, result):
        """Prikazi rezultat pretrage."""

        pag = Pagination(result, self.resultsPerPage)
        while True:
            print()
            currpage = pag.show()
            print("Pronađeno ukupno " + str(len(result)) + " rezultata.\n")
            for p in currpage:
                print(p)

            print()
            if pag.has_prev():
                print("P - Prethodna stranica rezultata")
            if pag.has_next():
                print("N - Sledeca stranica rezultata")
            print("O - Promena broja rezultata po stranici")
            print("M - Nazad na glavni meni")
            print("Bilo koji drugi karakter za povratak na pretragu.")
            op = input("\t>> ").lower()
            if op == "p" and pag.has_prev():
                pag.prev_page()
            elif op == "n" and pag.has_next():
                pag.next_page()
            elif op == "o":
                pag.set_per_page(self.change_results_per_page())
            elif op == "m":
                return False
            else:
                # TODO skontati zasto ovo nekad zapuca i ne ispise prompt za pretragu vec odmah ceka dalji unos
                # i to samo u pycharmu u powershellu ne
                return True

    def change_results_per_page(self):
        """Promeni broj rezultata prikazanih na jednoj stranici."""

        while True:
            try:
                print()
                i = int(input("Unesite zeljeni broj rezultata po stranici.\n\t>> "))
                self.resultsPerPage = i
                return i
            except ValueError:
                print("Unos mora biti broj!")

    def settings(self):
        """Promeni podesavanja stranica i rangiranja."""

        print()
        print("P - Izmena broja rezultata po stranici")
        print("R - Izmena parametara rangiranja")
        print("Bilo koji drugi karakter za povratak na glavni meni.")
        op = input("\t>> ").lower()
        if op == "p":
            self.change_results_per_page()
        elif op == "r":
            # TODO napraviti izmenu parametara rangiranja
            pass
        else:
            return

