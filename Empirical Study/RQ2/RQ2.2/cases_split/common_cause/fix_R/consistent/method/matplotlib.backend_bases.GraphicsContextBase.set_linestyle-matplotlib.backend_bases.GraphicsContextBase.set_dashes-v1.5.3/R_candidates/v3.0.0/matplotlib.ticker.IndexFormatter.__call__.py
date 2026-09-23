    def __call__(self, x, pos=None):
        """
        Return the format for tick value `x` at position pos.

        The position is ignored and the value is rounded to the nearest
        integer, which is used to look up the label.
        """
        i = int(x + 0.5)
        if i < 0 or i >= self.n:
            return ''
        else:
            return self.labels[i]
