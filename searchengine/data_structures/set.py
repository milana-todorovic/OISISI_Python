class Set:
    """Implementacija skupa zasnovana na upotrebi ugradjenog tipa dictionary.
    
    Namenjena za cuvanje skupa stranica koji sadrze odredjenu rec. Preklopljeni 
    operatori - (razlika), | (unija), i & (presek). Omoguceno cuvanje pomocnog
    podatka uz elemente skupa radi kasnijeg rangiranja rezultata pretrage.
    """
    
    def __init__(self, iterable=[]):
        """Inicijalizuj skup.
    
        Argumenti:
            iterable - elementi koje inicijalno treba ubaciti u skup. Ako se izostavi,
            skup ce biti prazan.
        """
        self.elements = {}
        # ideja 1 - kada se izvuce lista reci iz dokumenta, napraviti od nje set 
        # (koji sadrži i broj pojavljivanja svake reci)
        # zatim proci kroz sve elemente seta i dodavati u trie
        # (pri cemu se direktno ubacuje vec izracunati broj pojavljivanja)
        # potencijalno nije dobra ideja ako je prosecan broj pojavljivanja reci u dokumentu ~= 1 ?
        # ideja 2 - direktno prolaziti kroz listu reci i dodavati u trie
        # potencijalno lose ako je prosecan broj pojavljivanja >> 1 ? (vise puta se kroz trie dolazi do kraja iste reci)
        # probaj oboje, vidi sta je brze
        for elem in iterable:
            self.add(elem)

    def __len__(self):
        """Vrati broj elemenata u skupu."""
        return len(self.elements)

    def add(self, elem, val=1):
        """Dodaj element u skup.
        
        Parametri:
            elem - element koji treba dodati.
            val - opciona pomocna vrednost koja ce cuva uz element. U slucaju pokusaja
            visestrukog dodavanja istog elementa, pomocne vrednosti se akumuliraju. 
        """
        if elem in self.elements:
            self.elements[elem] += val
        else:
            self.elements[elem] = val

    def __contains__(self, elem):
        return elem in self.elements

    def __iter__(self):
        return self.elements.__iter__()

    def __sub__(self, other):
        """Vrati razliku skupova.
        
        Pomocne vrednosti se cuvaju iz levog skupa.
        """
        retVal = Set()
        for (elem, val) in self.elements.items():
            if elem not in other:
                retVal.add(elem, val)
        return retVal

    def __and__(self, other):
        """Vrati presek skupova.
        
        Pomocne vrednosti se sabiraju.
        """
        retVal = Set()
        if len(self) <= len(other):
            for (elem, val) in self.elements.items():
                if elem in other:
                    retVal.add(elem, val + other.elements[elem])
        else:
            for (elem, val) in other.elements.items():
                if elem in self:
                    retVal.add(elem, val + self.elements[elem])
        return retVal

    def __or__(self, other):
        """Vrati uniju skupova."""
        retVal = Set()
        for (elem, val) in self.elements.items():
            retVal.add(elem, val)
        for (elem, val) in other.elements.items():
            retVal.add(elem, val)
        return retVal

    def __str__(self):
        return str([elem for elem in self.elements.keys()])



