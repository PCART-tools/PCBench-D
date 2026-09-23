    def _extended_N(self):
        """
        Based on the colormap and extend variable, return the
        number of boundaries.
        """
        N = self.cmap.N + 1
        if self.extend == 'both':
            N += 2
        elif self.extend in ('min', 'max'):
            N += 1
        return N
