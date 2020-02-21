from searchengine.data_structures.set import Set


class TrieNode:
    """Klasa koja predstavlja cvor trie-a.

    Za cuvanje dece cvora koristi se ugradjeni tip dictionary, a vrednosti
    pridruzene cvoru se cuvaju u Set-u.
    """

    def __init__(self):
        self.children = {}
        self.pages = Set()


class Trie:
    """Implementaciija trie stabla zasnovana na tipovima dictionary i Set."""

    def __init__(self):
        """Inicijalizuj trie."""
        self.root = TrieNode()

    def add(self, word, page, val):
        """Dodaj rec u trie.

        Argumenti:
            word - rec koja se dodaje u trie.
            page - vrednost koja se pridruzuje cvoru koji oznacava kraj reci. Ukoliko
            se istoj reci pridruzi vise vrednosti, akumuliraju se u Set.
            val - vrednost pridruzena uz page u Setu.
        """
        currnode = self.root

        for letter in word:
            if letter not in currnode.children:
                currnode.children[letter] = TrieNode()
            currnode = currnode.children[letter]

        if currnode is not self.root:
            currnode.pages.add(page, val)

    def find(self, word):
        """Pronadji rec u trie stablu. Vrati pridruzenu vrednost uz rec.

        Ukoliko se rec ne nalazi u stablu, rezultat je prazan Set.
        """
        currnode = self.root

        for letter in word:
            if letter not in currnode.children:
                return Set()
            currnode = currnode.children[letter]

        return currnode.pages
