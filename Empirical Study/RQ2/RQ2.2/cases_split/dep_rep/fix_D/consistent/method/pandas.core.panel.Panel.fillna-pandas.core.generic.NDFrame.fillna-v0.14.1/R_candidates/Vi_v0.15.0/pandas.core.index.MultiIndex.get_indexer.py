    def get_indexer(self, target, method=None, limit=None):
        """
        Compute indexer and mask for new index given the current index. The
        indexer should be then used as an input to ndarray.take to align the
        current data to the new index. The mask determines whether labels are
        found or not in the current index

        Parameters
        ----------
        target : MultiIndex or Index (of tuples)
        method : {'pad', 'ffill', 'backfill', 'bfill'}
            pad / ffill: propagate LAST valid observation forward to next valid
            backfill / bfill: use NEXT valid observation to fill gap

        Notes
        -----
        This is a low-level method and probably should be used at your own risk

        Examples
        --------
        >>> indexer, mask = index.get_indexer(new_index)
        >>> new_values = cur_values.take(indexer)
        >>> new_values[-mask] = np.nan

        Returns
        -------
        (indexer, mask) : (ndarray, ndarray)
        """
        method = self._get_method(method)

        target = _ensure_index(target)

        target_index = target
        if isinstance(target, MultiIndex):
            target_index = target._tuple_index

        if target_index.dtype != object:
            return np.ones(len(target_index)) * -1

        if not self.is_unique:
            raise Exception('Reindexing only valid with uniquely valued Index '
                            'objects')

        self_index = self._tuple_index

        if method == 'pad':
            if not self.is_unique or not self.is_monotonic:
                raise AssertionError(('Must be unique and monotonic to '
                                      'use forward fill getting the indexer'))
            indexer = self_index._engine.get_pad_indexer(target_index.values,
                                                         limit=limit)
        elif method == 'backfill':
            if not self.is_unique or not self.is_monotonic:
                raise AssertionError(('Must be unique and monotonic to '
                                      'use backward fill getting the indexer'))
            indexer = self_index._engine.get_backfill_indexer(target_index.values,
                                                              limit=limit)
        else:
            indexer = self_index._engine.get_indexer(target_index.values)

        return com._ensure_platform_int(indexer)
