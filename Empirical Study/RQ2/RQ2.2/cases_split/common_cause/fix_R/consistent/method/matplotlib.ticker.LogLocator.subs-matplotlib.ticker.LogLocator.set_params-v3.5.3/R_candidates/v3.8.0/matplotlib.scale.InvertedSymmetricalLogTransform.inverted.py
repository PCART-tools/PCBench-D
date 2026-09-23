    def inverted(self):
        return SymmetricalLogTransform(self.base,
                                       self.linthresh, self.linscale)
