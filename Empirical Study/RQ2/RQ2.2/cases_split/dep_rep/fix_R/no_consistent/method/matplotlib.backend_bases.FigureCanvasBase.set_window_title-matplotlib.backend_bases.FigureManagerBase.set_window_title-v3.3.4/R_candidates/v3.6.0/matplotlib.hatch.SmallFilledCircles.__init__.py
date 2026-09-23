    def __init__(self, hatch, density):
        self.num_rows = (hatch.count('.')) * density
        super().__init__(hatch, density)
