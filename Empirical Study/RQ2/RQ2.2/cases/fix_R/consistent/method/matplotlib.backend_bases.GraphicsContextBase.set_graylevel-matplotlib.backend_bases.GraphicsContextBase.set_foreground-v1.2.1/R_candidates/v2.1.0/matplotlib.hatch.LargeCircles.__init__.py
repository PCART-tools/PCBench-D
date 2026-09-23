    def __init__(self, hatch, density):
        self.num_rows = (hatch.count('O')) * density
        Circles.__init__(self, hatch, density)
