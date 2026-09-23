    def __init__(self, hatch, density):
        self.num_rows = (hatch.count('o')) * density
        Circles.__init__(self, hatch, density)
