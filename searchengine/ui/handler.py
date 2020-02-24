from datetime import datetime
import os

from searchengine.core.engine import SearchEngine
from searchengine.query.simple_query import SimpleQueryError
from searchengine.query.complex_query import ComplexQueryError
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
            print("Q - Napredna pretraga")
            print("C - Promena direktorijuma za pretragu")
            print("O - Ostale postavke")
            print("Bilo koji drugi karakter za završetak rada.")
            op = input("\t>> ").lower()
            if op == "s":
                self.simple_search()
            elif op == "q":
                self.complex_search()
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
            if not os.path.isdir(rootdir):
                print("Unesena putanja nije postojeći direktorijum!")
                continue
            try:
                absdir = os.path.abspath(rootdir)
            except Exception:
                print("Greška pri konverziji putanje!")
                continue
            print("Učitavanje...")
            start = datetime.now()
            if self.engine.loadroot(absdir):
                print("Učitavanje uspešno. Utrošeno vreme: " + str(datetime.now() - start))
                wrong = False
            else:
                print("Greška pri učitavanju ili direktorijum ne sadrži html faljove!")

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
                    print("\nUtrošeno vreme: " + str(datetime.now() - start))
                    search = self.show_search_result(res)
                except SimpleQueryError as err:
                    print(err.message)

    def complex_search(self):
        """Pretrazi po upitu sa naprednom upotrebom logickih operatora."""

        search = True
        while search:
            print()
            query = input("Unesite upit (enter za povratak na glavni meni).\n\t>> ")
            if query == "":
                search = False
            else:
                try:
                    start = datetime.now()
                    res = self.engine.complex_search(query)
                    print("\nUtrošeno vreme: " + str(datetime.now() - start))
                    search = self.show_search_result(res)
                except ComplexQueryError:
                    print("Greška u upitu!")

    def show_search_result(self, result):
        """Prikazi rezultat pretrage."""

        pag = Pagination(result, self.resultsPerPage)
        numres = len(result)
        while True:
            print()
            currpage = pag.show()
            print("Pronađeno ukupno " + str(numres) + " rezultata.")
            if numres > 0:
                print()
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
                # u vscode isto ne
                return True

    def change_results_per_page(self):
        """Promeni broj rezultata prikazanih na jednoj stranici."""

        while True:
            try:
                print()
                i = int(input("Unesite zeljeni broj rezultata po stranici.\n\t>> "))
                if i <= 0:
                    raise ValueError()
                self.resultsPerPage = i
                return i
            except ValueError:
                print("Unos mora biti prirodan broj!")

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
            self.edit_ranking_params()
        else:
            return

    def edit_ranking_params(self):
        """Promeni podesavanja rangiranja."""

        print()
        print("P - Izmena uticaja broja reci i linkova")
        print("O - Izmena uticaja or upita")
        # TODO dozvoliti ovo ili ne?
        #print("D - Izmena dubine obilaska grafa pri racunanju uticaja linkova")
        print("Bilo koji drugi karakter za povratak na glavni meni.")
        op = input("\t>> ").lower()
        if op == "p":
            self.edit_influences()
        elif op == "o":
            self.edit_or_factor()
        #elif op == "d":
            #self.edit_depth()
        else:
            return

    def edit_or_factor(self):
        wrong = True

        while wrong:
            try:
                print()
                print("Unesite željeni faktor uticaja or upita.")
                print("Ocekivana vrednost: izmedju 0 i 1.")
                print("Trenutna vrednost: " + str(self.engine.rParams.orWeight))
                i = float(input("Nova vrednost:\t>> "))
                if i < 0:
                    raise ValueError()
                self.engine.set_or_weight(i)
                wrong = False
            except ValueError:
                print("Unos mora biti nenegativan broj!")

    def edit_influences(self):
        wrong = True

        while wrong:
            try:
                print()
                print("Unesite željene procente uticaja. Zbir mora biti 100.")
                print("Trenutna vrednost uticaja reci: " + str(self.engine.rParams.wordInf))
                print("Trenutna vrednost uticaja relevantnih linkova: " + str(self.engine.rParams.relevantLinkInf))
                print("Trenutna vrednost uticaja svih linkova: " + str(self.engine.rParams.generalLinkInf))
                w = float(input("Novi uticaj reci:\t>> "))
                rl = float(input("Novi uticaj relevantnih linkova:\t>> "))
                gl = float(input("Novi uticaj svih linkova:\t>> "))
                if w < 0 or rl < 0 or gl < 0:
                    print("Vrednosti moraju biti pozitivne!")
                    continue
                if w + rl + gl != 100:
                    print("Zbir vrednosti mora biti 100!")
                    continue
                self.engine.set_influences(w, rl, gl)
                wrong = False
            except ValueError:
                print("Uneta vrednost mora biti broj!")

    def edit_depth(self):
        wrong = True

        while wrong:
            try:
                print()
                print("Unesite željenu dubinu obilaska grafa.")
                print("Ocekivana vrednost: pozitivan broj ili None.")
                print("Preporučena vrednost: maksimalno 2. Veće vrednosti mogu izazvati značajnu degradaciju performansi!")
                print("Trenutna vrednost: " + str(self.engine.rParams.depth))
                val = input("Nova vrednost:\t>> ").lower()
                if val == "none":
                    self.engine.set_depth(None)
                    wrong = False
                else:
                    i = int(val)
                    if i <= 0:
                        raise ValueError()
                    self.engine.set_depth(i)
                    wrong = False
            except ValueError:
                print("Unos mora biti prirodan broj ili None!")
