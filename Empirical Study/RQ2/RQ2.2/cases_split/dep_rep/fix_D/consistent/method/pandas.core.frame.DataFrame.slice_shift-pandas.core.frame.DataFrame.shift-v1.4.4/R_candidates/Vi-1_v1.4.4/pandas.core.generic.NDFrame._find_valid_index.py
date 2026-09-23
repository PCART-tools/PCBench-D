    @final
    def _find_valid_index(self, *, how: str) -> Hashable | None:
        """
        Retrieves the index of the first valid value.

        Parameters
        ----------
        how : {'first', 'last'}
            Use this parameter to change between the first or last valid index.

        Returns
        -------
        idx_first_valid : type of index
        """
        idxpos = find_valid_index(self._values, how=how)
        if idxpos is None:
            return None
        return self.index[idxpos]
