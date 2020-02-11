from searchengine.data_structures.graph import Graph
from searchengine.data_structures.set import Set

class RankData:
    # TODO dodati poene za broj ispunjenih uslova u or izrazima? 

    def __init__(self, words=1, links=0):
        self.wScore = words
        self.lScore = links

    def __add__(self, other):
        return RankData(self.wScore + other.wScore, self.lScore + other.lScore)

    def __iadd__(self, other):
        self.wScore += other.wScore
        self.lScore += other.lScore
        return self

    def __int__(self):
        return int(self.lScore + self.wScore)


class RankResult:
    def __init__(self, path, rank:RankData):
        self.path = path
        self.rank = rank

    def __int__(self):
        return int(self.rank)

    def __gt__(self, other):
        return int(self) > int(other)



def calculate_rank(graph:Graph, searchResult:Set, decay, depth):
    for page in searchResult:
        for pg, d in graph.bft(page, depth):
            if d>0 and pg in searchResult:
                searchResult.add(pg, RankData(0, decay**(d-1)))

    ranked = [RankResult(page, searchResult.elements[page]) for page in searchResult]
    return radix(ranked)


def radix(iterable):
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


    
