    def __init__(self, hatch, density):
        self.num_rows = (hatch.count('.')) * density
        Circles.__init__(self, hatch, density)
