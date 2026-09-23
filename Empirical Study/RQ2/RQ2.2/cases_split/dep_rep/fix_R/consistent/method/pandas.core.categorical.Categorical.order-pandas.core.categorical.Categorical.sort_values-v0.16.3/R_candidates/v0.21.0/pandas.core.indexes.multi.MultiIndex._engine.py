    @cache_readonly
    def _engine(self):

        # choose our engine based on our size
        # the hashing based MultiIndex for larger
        # sizes, and the MultiIndexOjbect for smaller
        # xref: https://github.com/pandas-dev/pandas/pull/16324
        l = len(self)
        if l > 10000:
            return libindex.MultiIndexHashEngine(lambda: self, l)

        return libindex.MultiIndexObjectEngine(lambda: self.values, l)
