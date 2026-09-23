    def mode(self):
        """
        Returns the mode(s) of the Categorical.

        Always returns `Categorical` even if only one value.

        Returns
        -------
        modes : `Categorical` (sorted)
        """

        import pandas._libs.hashtable as htable
        good = self._codes != -1
        values = sorted(htable.mode_int64(_ensure_int64(self._codes[good])))
        result = self._constructor(values=values, categories=self.categories,
                                   ordered=self.ordered, fastpath=True)
        return result
