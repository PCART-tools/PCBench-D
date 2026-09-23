    def mode(self):
        """
        Returns the mode(s) of the Categorical.

        Empty if nothing occurs at least 2 times.  Always returns `Categorical` even
        if only one value.

        Returns
        -------
        modes : `Categorical` (sorted)
        """

        import pandas.hashtable as htable
        good = self._codes != -1
        result = Categorical(sorted(htable.mode_int64(com._ensure_int64(self._codes[good]))),
                             categories=self.categories,ordered=self.ordered, name=self.name,
                             fastpath=True)
        return result
