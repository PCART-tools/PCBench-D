    def _find_valid_index(self, how):
        """Retrieves the index of the first valid value.

        Parameters
        ----------
        how : {'first', 'last'}
            Use this parameter to change between the first or last valid index.

        Returns
        -------
        idx_first_valid : type of index
        """
        assert how in ['first', 'last']

        if len(self) == 0:  # early stop
            return None
        is_valid = ~self.isna()

        if self.ndim == 2:
            is_valid = is_valid.any(1)  # reduce axis 1

        if how == 'first':
            idxpos = is_valid.values[::].argmax()

        if how == 'last':
            idxpos = len(self) - 1 - is_valid.values[::-1].argmax()

        chk_notna = is_valid.iat[idxpos]
        idx = self.index[idxpos]

        if not chk_notna:
            return None
        return idx
