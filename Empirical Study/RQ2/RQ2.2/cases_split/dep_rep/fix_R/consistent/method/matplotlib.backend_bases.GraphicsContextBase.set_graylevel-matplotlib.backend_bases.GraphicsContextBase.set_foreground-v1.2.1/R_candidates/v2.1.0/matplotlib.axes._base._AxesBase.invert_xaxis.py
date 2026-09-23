    def invert_xaxis(self):
        "Invert the x-axis."
        left, right = self.get_xlim()
        self.set_xlim(right, left, auto=None)
