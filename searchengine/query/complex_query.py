import parglare

from searchengine.data_structures.trie import Trie
from searchengine.data_structures.set import Set


class OrNode:
    """Klasa koja predstavlja or izraz u stablu medjukoda."""

    def __init__(self, leftOperand, rightOperand):
        self.leftOperand = leftOperand
        self.rightOperand = rightOperand

    def evaluate(self, trie:Trie, allPages:Set):
        """Evaluiraj podstablo i vrati uniju."""
        return self.leftOperand.evaluate(trie, allPages) | self.rightOperand.evaluate(trie, allPages)


class AndNode:
    """Klasa koja predstavlja and izraz u stablu medjukoda."""

    def __init__(self, leftOperand, rightOperand):
        self.leftOperand = leftOperand
        self.rightOperand = rightOperand

    def evaluate(self, trie:Trie, allPages:Set):
        """Evaluiraj podstablo i vrati presek."""
        return self.leftOperand.evaluate(trie, allPages) & self.rightOperand.evaluate(trie, allPages)


class NotNode:
    """Klasa koja predstavlja not izraz u stablu medjukoda."""

    def __init__(self, operand):
        self.operand = operand

    def evaluate(self, trie:Trie, allPages:Set):
        """Evaluiraj podstablo i vrati razliku."""
        return allPages - self.operand.evaluate(trie, allPages)


class WordNode:
    """Klasa koja predstavlja rec u stablu medjukoda."""

    def __init__(self, word):
        self.word = word

    def evaluate(self, trie:Trie, allPages:Set):
        """Evaluiraj podstablo i vrati skup stranica koje sadrže reč."""
        return trie.find(self.word.lower())


class ComplexQueryError(Exception):
    """Klasa koja predstavlja gresku pri parsiranju kompleksnog upita."""

    def __init__(self):
        self.message = "Greška pri parsiranju kompleksnog upita!"


class ComplexQueryParser:
    """Klasa koja predstavlja parser kompleksnih upita, zasnovan na alatu parglare."""

    def __init__(self):
        """Inicijalizuj parglare parser na osnovu gramatike kompleksnih upita."""

        # TODO moze li se ovo naterati da prepoznaje & i | kao reci??
        grammar_string = r"""
        expression: oroperand
                  | expression oroperand
                  | expression '||' oroperand
                  ;
        
        oroperand: andoperand
                 | oroperand '&&' andoperand
                 ;

        andoperand: notoperand
                  | '!' notoperand
                  ;
        
        notoperand: word
                  | '(' expression ')'
                  ;

        terminals
        word: /[^&|!() \t\n]+/
            ;
        """

        actions = {
            "expression" : [lambda _, nodes: nodes[0],
                            lambda _, nodes: OrNode(nodes[0], nodes[1]),
                            lambda _, nodes: OrNode(nodes[0], nodes[2])],
            "oroperand"  : [lambda _, nodes: nodes[0],
                            lambda _, nodes: AndNode(nodes[0], nodes[2])],
            "andoperand" : [lambda _, nodes: nodes[0],
                            lambda _, nodes: NotNode(nodes[1])],
            "notoperand" : [lambda _, nodes: nodes[0],
                            lambda _, nodes: nodes[1]],
            "word"       : lambda _, value: WordNode(value),
        }

        grammar = parglare.Grammar.from_string(grammar_string)
        self.parser = parglare.Parser(grammar, actions=actions)

    def parse(self, query):
        """Parsiraj upit i vrati stablo medjukoda."""

        try:
            return self.parser.parse(query)
        except parglare.exceptions.ParseError:
            raise ComplexQueryError()
