class SmallFilledCircles(SmallCircles):
    size = 0.1
    filled = True

    def __init__(self, hatch, density):
        self.num_rows = (hatch.count('.')) * density
        # Not super().__init__!
        Circles.__init__(self, hatch, density)
