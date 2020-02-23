import itertools

from searchengine.data_structures.graph import Graph
from searchengine.data_structures.set import Set

# TODO dodati uticaj broja reci u or upitima u rangiranje


class RankingParameters:
    """Klasa koja sadrzi parametre koji uticu na rangiranje."""

    def __init__(self, wordInfluence=50, relevantLinkInfluence=40, generalLinkInfluence=10, orWeight=0.5, depth=2):
        """Inicijalizacija parametara rangirnja.

        Argumenti:
            wordInfluence - procenat ranga stranice koji odredjuje broj pronadjenih reci.
            linkInfluence - procenat ranga stranice koji odredjuju linkovi na stranicu.
            initialLinkWeight - uticaj na rang linkova sa stranica koje ne sadrze trazene
            reci. Vrijednost N znaci da ce svaka stranica koja ne sadrzi rec uticati na
            rang kao da sadrzi N reci, a stranica koja sadrzi M reci ce uticati kao da 
            sadrzi M + N reci.
            decay - koeficijent kojim se mnozi broj reci u stranici pri racunanju njenog
            uticaja na rang stranica koje linkuje.
            depth - dubina do koje linkovi imaju uticaj. 
        """
        self.wordInf = wordInfluence
        self.relevantLinkInf = relevantLinkInfluence
        self.generalLinkInf = generalLinkInfluence
        self.orWeight = orWeight
        self.depth = depth


class RankData:
    def __init__(self, wordScore, orScore):
        self.wordScore = wordScore
        self.orScore = orScore

    def __add__(self, other):
        # ovu operaciju poziva presjek
        return RankData(self.wordScore + other.wordScore, max(self.orScore, other.orScore))

    def __iadd__(self, other):
        # ovu operaciju pozivaju unija i dodavanje u skup
        # dodavanje je pravljeno tako da ce se pri inicijalnom pravljenju trie strukture
        # za svaku rec stranica dodati samo jednom
        # tako da je inicijalni orScore za svaku stranicu 1
        self.wordScore += other.wordScore
        self.orScore += other.orScore
        return self


class RankResult:
    """Klasa koja predstavlja stranicu sa izracunatim rangom."""

    def __init__(self, path, wordScore, relevantLinkScore, generalLinkScore, orScore, orWeight):
        self.path = path
        self.wordScore = wordScore
        self.relLinkScore = relevantLinkScore
        self.genLinkScore = generalLinkScore
        self.orScore = orScore
        orFactor = (orScore - 1)*orWeight + 1
        self.rank = int((wordScore + relevantLinkScore + generalLinkScore)*orFactor)

    def __int__(self):
        return self.rank

    def __gt__(self, other):
        return int(self) > int(other)

    def __str__(self):
        strformat = "{}:\n\tReci: {:.2f}\tRelevantni linkovi: {:.2f}\tSvi linkovi: {:.2f}\tOr: {}\tUkupno: {}"
        return strformat.format(self.path, self.wordScore, self.relLinkScore, self.genLinkScore, self.orScore, self.rank)


def rank_and_sort(graph:Graph, searchResult:Set, initLinkScores:dict, params:RankingParameters):
    """Izracunaj rang stranica i sortiraj ih po izracunatom rangu.
    
    Argumenti:
        graph - graf koji sadrzi linkove izmedju stranica.
        pages - stranice za koje se racuna uticaj linkova na rang. Pridruzene vrednosti
        u skupu predstavljaju uticaj koji stranica ima na rang linkovanih stranica.
        depth - dubina do koje se obilazi graf.
        decay - faktor opadanja uticaja sa dubinom.
    """
    if len(searchResult) == 0:
        return []
    else:
        return radix(calculate_rank(graph, searchResult, initLinkScores, params))


def calculate_link_scores(graph:Graph, pages:Set, depth):
    """Izracunaj uticaj linkova na rang.
    
    Argumenti:
        graph - graf koji sadrzi linkove izmedju stranica.
        pages - stranice za koje se racuna uticaj linkova na rang. Pridruzene vrednosti
        u skupu predstavljaju uticaj koji stranica ima na rang linkovanih stranica.
        depth - dubina do koje se obilazi graf.
        decay - faktor opadanja uticaja sa dubinom.
    """

    # pripremi povratnu vrednost - O(n)
    scores = dict(zip(pages, itertools.repeat(0)))

    # spoljasnja petlja - O(n)
    for page in pages:
        val = int(pages.elements[page])
        # unutrasnja petlja - zavisi od depth
        # me - maksimalan broj ivica koje izlaze iz cvora u grafu
        # depth = 1 -> O(me)
        # depth = 2 -> O(me^2)
        # depth->Inf -> O(e)
        for pg, lnum, d in graph.bfs(page, depth):
            if d>0 and pg in scores and pg != page:
                scores[pg] += val/lnum
    # sve ukupno - O(e) za d=1 i n=v
    # O(n*e) za d->Inf 

    return scores

       
def calculate_rank(graph:Graph, searchResult:Set, initLinkScores:dict, params:RankingParameters):
    """Izracunaj rang stranica i vrati iterator kroz stranice sa pridruzenim rangom.
    
    Argumenti:
        graph - graf koji sadrzi linkove izmedju stranica.
        searchResult - neprazan skup stranica koje se rangiraju. Pridruzene vrednosti u skupu se posmatraju
        kao broj reci u stranici.
        initLinkScores - inicijalni rang izracunat na osnovu linkova.
        params - parametri potrebni za rangiranje.
    """

    # odvoji skor od reci od skora za or - O(n)
    wordsOnly = Set()
    for page in searchResult:
        wordsOnly.add(page, searchResult.elements[page].wordScore)

    # izracuna skor za linkove - O(e) za samo direktne, O(n*e) za citav graf, nesto izmedju trenutno
    linkScores = calculate_link_scores(graph, wordsOnly, params.depth) 
    wordScores = wordsOnly.elements

    # trazi maksimume za skaliranje - O(n)
    wordMax = max(wordScores.values())
    if wordMax == 0:
        wordMax = 1
    wordInf = params.wordInf

    linkMax = max(linkScores.values())
    if linkMax == 0:
        linkMax = 1
    linkInf = params.relevantLinkInf

    genLinkMax = max(initLinkScores.values())
    if genLinkMax == 0:
        genLinkMax = 1
    genLinkInf = params.generalLinkInf

    # vraca stranice jednu po jednu jer radix svakako prvo pravi listu
    for page in searchResult:
        wScore = wordScores[page]/wordMax*wordInf*10
        relLinkScore = linkScores[page]/linkMax*linkInf*10
        genLinkScore = initLinkScores[page]/genLinkMax*genLinkInf*10
        yield RankResult(page, wScore, relLinkScore, genLinkScore, searchResult.elements[page].orScore, params.orWeight)


def radix(iterable):
    """Implementacija radix sort algoritma.

    Argumenti:
        iterable - sadrzi elemente koje treba sortirati. Ne sme biti prazan. Elementi moraju imati 
        implementirane metode __int__ i __gt__.
    """

    # pretvori iterable u listu - O(n)
    retVal = list(iterable)
    # max u listi - O(n)
    val = max(retVal)
    mask = 1

    # sam radix - O(n)
    while mask < 2*int(val):
        zero = []
        one = []
        for elem in retVal:
            if mask & int(elem) == 0:
                zero.append(elem)
            else:
                one.append(elem)
        retVal = one
        retVal.extend(zero)
        mask <<= 1

    return retVal


    
