class SimpleQueryError(Exception):
    """Klasa koja predstavlja gresku pri parsiranju osnovnih upita."""

    def __init__(self, message):
        self.message = message


def parse(query):
    """Parsiraj osnovni upit i vrati listu reci i operator.

    U slucaju greske podize SimpleQueryError sa odgovarajucom porukom.
    Argumenti:
        query - upit.
    """

    reci = query.lower().strip().split()

    if not reci:
        raise SimpleQueryError("Upit mora sadržati bar jednu reč!")

    andcount = reci.count("and")
    orcount = reci.count("or")
    notcount = reci.count("not")

    if (andcount + orcount + notcount) > 1:
        raise SimpleQueryError("Upit može sadržati maksimalno jedan logički operator!")

    if andcount == 1:
        if len(reci) != 3 or reci[1] != "and":
            raise SimpleQueryError("Operator and može biti samo između dve reči!")
        else:
            return [rec for rec in reci if rec != "and"], "and"
    elif notcount == 1:
        if len(reci) != 3 or reci[1] != "not":
            raise SimpleQueryError("Operator not može biti samo između dve reči!")
        else:
            return [rec for rec in reci if rec != "not"], "not"
    elif orcount == 1:
        if len(reci) != 3 or reci[1] != "or":
            raise SimpleQueryError("Operator or može biti samo između dve reči!")
        else:
            return [rec for rec in reci if rec != "or"], "or"
    else:
        return reci, "or"
