    def invert(self):
        """ invert the filter """
        if self.filter is not None:
            f = list(self.filter)
            f[1] = self.generate_filter_op(invert=True)
            self.filter = tuple(f)
        return self
