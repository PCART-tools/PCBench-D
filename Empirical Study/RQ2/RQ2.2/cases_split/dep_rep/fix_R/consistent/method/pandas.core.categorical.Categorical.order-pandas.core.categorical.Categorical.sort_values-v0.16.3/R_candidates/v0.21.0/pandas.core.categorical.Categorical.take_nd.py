    def take_nd(self, indexer, allow_fill=True, fill_value=None):
        """ Take the codes by the indexer, fill with the fill_value.

        For internal compatibility with numpy arrays.
        """

        # filling must always be None/nan here
        # but is passed thru internally
        assert isna(fill_value)

        codes = take_1d(self._codes, indexer, allow_fill=True, fill_value=-1)
        result = self._constructor(codes, categories=self.categories,
                                   ordered=self.ordered, fastpath=True)
        return result
