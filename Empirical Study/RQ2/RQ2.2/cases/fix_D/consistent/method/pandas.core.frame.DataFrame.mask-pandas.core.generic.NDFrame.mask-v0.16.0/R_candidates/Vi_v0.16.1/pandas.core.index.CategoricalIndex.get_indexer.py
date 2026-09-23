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
        method = com._clean_reindex_fill_method(method)
        target = _ensure_index(target)

        if isinstance(target, CategoricalIndex):
            target = target.categories

        if method == 'pad' or method == 'backfill':
            raise NotImplementedError("method='pad' and method='backfill' not implemented yet "
                                      'for CategoricalIndex')
        elif method == 'nearest':
            raise NotImplementedError("method='nearest' not implemented yet "
                                      'for CategoricalIndex')
        else:

            codes = self.categories.get_indexer(target)
            indexer, _ = self._engine.get_indexer_non_unique(codes)

        return com._ensure_platform_int(indexer)
