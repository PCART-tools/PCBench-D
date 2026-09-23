    def __init__(self, hatch, density):
        self.num_rows = (hatch.count('.')) * density
        # Not super().__init__!
        Circles.__init__(self, hatch, density)
