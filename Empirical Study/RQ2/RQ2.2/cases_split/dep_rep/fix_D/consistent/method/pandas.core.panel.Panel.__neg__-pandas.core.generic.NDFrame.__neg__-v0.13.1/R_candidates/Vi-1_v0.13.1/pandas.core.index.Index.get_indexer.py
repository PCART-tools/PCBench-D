    def get_indexer(self, target, method=None, limit=None):
        """
        Compute indexer and mask for new index given the current index. The
        indexer should be then used as an input to ndarray.take to align the
        current data to the new index. The mask determines whether labels are
        found or not in the current index

        Parameters
        ----------
        target : Index
        method : {'pad', 'ffill', 'backfill', 'bfill'}
            pad / ffill: propagate LAST valid observation forward to next valid
            backfill / bfill: use NEXT valid observation to fill gap

        Notes
        -----
        This is a low-level method and probably should be used at your own risk

        Examples
        --------
        >>> indexer = index.get_indexer(new_index)
        >>> new_values = cur_values.take(indexer)

        Returns
        -------
        indexer : ndarray
        """
        method = self._get_method(method)
        target = _ensure_index(target)

        pself, ptarget = self._possibly_promote(target)
        if pself is not self or ptarget is not target:
            return pself.get_indexer(ptarget, method=method, limit=limit)

        if self.dtype != target.dtype:
            this = self.astype(object)
            target = target.astype(object)
            return this.get_indexer(target, method=method, limit=limit)

        if not self.is_unique:
            raise InvalidIndexError('Reindexing only valid with uniquely'
                                    ' valued Index objects')

        if method == 'pad':
            if not self.is_monotonic or not target.is_monotonic:
                raise ValueError('Must be monotonic for forward fill')
            indexer = self._engine.get_pad_indexer(target.values, limit)
        elif method == 'backfill':
            if not self.is_monotonic or not target.is_monotonic:
                raise ValueError('Must be monotonic for backward fill')
            indexer = self._engine.get_backfill_indexer(target.values, limit)
        elif method is None:
            indexer = self._engine.get_indexer(target.values)
        else:
            raise ValueError('unrecognized method: %s' % method)

        return com._ensure_platform_int(indexer)
