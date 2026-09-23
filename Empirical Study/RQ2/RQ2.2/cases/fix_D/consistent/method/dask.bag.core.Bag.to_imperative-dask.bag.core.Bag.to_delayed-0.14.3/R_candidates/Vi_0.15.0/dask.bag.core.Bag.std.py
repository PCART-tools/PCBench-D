    def std(self, ddof=0):
        """ Standard deviation """
        return self.var(ddof=ddof).apply(math.sqrt)
