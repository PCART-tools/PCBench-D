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
        indexer, keyarr = super(MultiIndex, self)._convert_listlike_indexer(
            keyarr, kind=kind)

        # are we indexing a specific level
        if indexer is None and len(keyarr) and not isinstance(keyarr[0],
                                                              tuple):
            level = 0
            _, indexer = self.reindex(keyarr, level=level)

            # take all
            if indexer is None:
                indexer = np.arange(len(self))

            check = self.levels[0].get_indexer(keyarr)
            mask = check == -1
            if mask.any():
                raise KeyError('%s not in index' % keyarr[mask])

        return indexer, keyarr
