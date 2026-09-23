    def _getitem_iterable(self, key, axis=None):
        """
        Index current object with an an iterable key (which can be a boolean
        indexer, or a collection of keys).

        Parameters
        ----------
        key : iterable
            Target labels, or boolean indexer
        axis: int, default None
            Dimension on which the indexing is being made

        Raises
        ------
        KeyError
            If no key was found. Will change in the future to raise if not all
            keys were found.
        IndexingError
            If the boolean indexer is unalignable with the object being
            indexed.

        Returns
        -------
        scalar, DataFrame, or Series: indexed value(s),
        """

        if axis is None:
            axis = self.axis or 0

        self._validate_key(key, axis)

        labels = self.obj._get_axis(axis)

        if com.is_bool_indexer(key):
            # A boolean indexer
            key = check_bool_indexer(labels, key)
            inds, = key.nonzero()
            return self.obj._take(inds, axis=axis)
        else:
            # A collection of keys
            keyarr, indexer = self._get_listlike_indexer(key, axis,
                                                         raise_missing=False)
            return self.obj._reindex_with_indexers({axis: [keyarr, indexer]},
                                                   copy=True, allow_dups=True)
