    def _convert_listlike_indexer(self, keyarr, kind=None):
        """
        Parameters
        ----------
        keyarr : list-like
            Indexer to convert.

        Returns
        -------
        tuple (indexer, keyarr)
            indexer is an ndarray or None if cannot convert
            keyarr are tuple-safe keys
        """
        if isinstance(keyarr, Index):
            keyarr = self._convert_index_indexer(keyarr)
        else:
            keyarr = self._convert_arr_indexer(keyarr)

        indexer = self._convert_list_indexer(keyarr, kind=kind)
        return indexer, keyarr
