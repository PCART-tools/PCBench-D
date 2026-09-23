    def get_indexer(self, target, method=None, limit=None):
        """
        Compute indexer and mask for new index given the current index. The
        indexer should be then used as an input to ndarray.take to align the
        current data to the new index.

        Parameters
        ----------
        target : Index
        method : {None, 'pad'/'ffill', 'backfill'/'bfill', 'nearest'}
            * default: exact matches only.
            * pad / ffill: find the PREVIOUS index value if no exact match.
            * backfill / bfill: use NEXT index value if no exact match
            * nearest: use the NEAREST index value if no exact match. Tied
              distances are broken by preferring the larger index value.
        limit : int
            Maximum number of consecuctive labels in ``target`` to match for
            inexact matches.

        Examples
        --------
        >>> indexer = index.get_indexer(new_index)
        >>> new_values = cur_values.take(indexer)

        Returns
        -------
        indexer : ndarray of int
            Integers from 0 to n - 1 indicating that the index at these
            positions matches the corresponding target values. Missing values
            in the target are marked by -1.
        """
        method = com._clean_reindex_fill_method(method)
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

        if method == 'pad' or method == 'backfill':
            indexer = self._get_fill_indexer(target, method, limit)
        elif method == 'nearest':
            indexer = self._get_nearest_indexer(target, limit)
        else:
            indexer = self._engine.get_indexer(target.values)

        return com._ensure_platform_int(indexer)
