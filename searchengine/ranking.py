import itertools

from searchengine.data_structures.graph import Graph
from searchengine.data_structures.set import Set

# TODO dodati uticaj broja reci u or upitima u rangiranje


class RankingParameters:
    """Klasa koja sadrzi parametre koji uticu na rangiranje."""

    def __init__(self, wordInfluence=50, linkInfluence=50, initialLinkWeight=1, decay=0.8, depth=2):
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
        self.wordInfluence = wordInfluence
        self.linkInfluence = linkInfluence
        self.initLinkWeight = initialLinkWeight
        self.decay = decay
        self.depth = depth


class RankResult:
    """Klasa koja predstavlja stranicu sa izracunatim rangom."""

    def __init__(self, path, wordScore, linkScore):
        self.path = path
        self.wordScore = wordScore
        self.linkScore = linkScore
        self.rank = int(wordScore + linkScore)

    def __int__(self):
        return self.rank

    def __gt__(self, other):
        return int(self) > int(other)

    def __str__(self):
        return self.path + "\t" + str(self.rank)


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


def calculate_link_scores(graph:Graph, pages:Set, depth, decay):
    """Izracunaj uticaj linkova na rang.
    
    Argumenti:
        graph - graf koji sadrzi linkove izmedju stranica.
        pages - stranice za koje se racuna uticaj linkova na rang. Pridruzene vrednosti
        u skupu predstavljaju uticaj koji stranica ima na rang linkovanih stranica.
        depth - dubina do koje se obilazi graf.
        decay - faktor opadanja uticaja sa dubinom.
    """

    # TODO dodati da broj linkova koje stranica sadrzi utice na skor koji ona prenosi 
    # stranicama koje linkuje? (po uzoru na PageRank)

    scores = dict(zip(pages, itertools.repeat(0)))

    for page in pages:
        val = pages.elements[page]
        for pg, d in graph.bfs(page, depth):
            if d>0 and pg in scores and pg != page:
                scores[pg] += val * decay**d

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

    linkScores = calculate_link_scores(graph, searchResult, params.depth, params.decay)
    finalLinkScores = {}
    for page in linkScores:
        finalLinkScores[page] = linkScores[page] + params.initLinkWeight * initLinkScores[page]
    wordScores = searchResult.elements

    wordMax = max(wordScores.values())
    if wordMax == 0:
        wordMax = 1
    wordInf = params.wordInfluence
    linkMax = max(finalLinkScores.values())
    if linkMax == 0:
        linkMax = 1
    linkInf = params.linkInfluence

    for page in searchResult:
        yield RankResult(page, wordScores[page]/wordMax*wordInf*10, finalLinkScores[page]/linkMax*linkInf*10)


def radix(iterable):
    """Implementacija radix sort algoritma.

    Argumenti:
        iterable - sadrzi elemente koje treba sortirati. Ne sme biti prazan. Elementi moraju imati 
        implementirane metode __int__ i __gt__.
    """

    retVal = list(iterable)
    val = max(retVal)
    mask = 1

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


    
