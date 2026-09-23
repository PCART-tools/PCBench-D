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
        is_valid = self.notna().values
        idxpos = find_valid_index(how=how, is_valid=is_valid)
        if idxpos is None:
            return None
        return self.index[idxpos]
