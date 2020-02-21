class Pagination:
    def __init__(self, sequence, perPage):
        self.elements = sequence
        self.numEl = len(sequence)
        self.pos = 0
        self.perPage = perPage

    def show(self):
        return self.elements[self.pos : self.pos + self.perPage]

    def has_next(self):
        return self.numEl - (self.pos + self.perPage) >= 1

    def has_prev(self):
        return self.pos > 0

    def next_page(self):
        self.pos += self.perPage

    def prev_page(self):
        self.pos -= self.perPage

    def set_per_page(self, perPage):
        self.perPage = perPage
        self.pos = self.pos//perPage*perPage
