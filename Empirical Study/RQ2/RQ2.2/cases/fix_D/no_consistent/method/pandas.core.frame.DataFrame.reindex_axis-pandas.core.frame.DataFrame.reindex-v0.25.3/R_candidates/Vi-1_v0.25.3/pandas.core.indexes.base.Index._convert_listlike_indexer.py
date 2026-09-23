    def _convert_listlike_indexer(self, keyarr, kind=None):
        """
        Parameters
        ----------
        keyarr : list-like
            Indexer to convert.

        Returns
        -------
        indexer : numpy.ndarray or None
            Return an ndarray or None if cannot convert.
        keyarr : numpy.ndarray
            Return tuple-safe keys.
        """
        if isinstance(keyarr, Index):
            keyarr = self._convert_index_indexer(keyarr)
        else:
            keyarr = self._convert_arr_indexer(keyarr)

        indexer = self._convert_list_indexer(keyarr, kind=kind)
        return indexer, keyarr
