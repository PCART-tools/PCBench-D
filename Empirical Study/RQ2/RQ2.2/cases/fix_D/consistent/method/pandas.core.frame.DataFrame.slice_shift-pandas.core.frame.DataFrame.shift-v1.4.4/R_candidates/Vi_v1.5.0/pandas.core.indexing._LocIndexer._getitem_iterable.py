    def _getitem_iterable(self, key, axis: int):
        """
        Index current object with an iterable collection of keys.

        Parameters
        ----------
        key : iterable
            Targeted labels.
        axis : int
            Dimension on which the indexing is being made.

        Raises
        ------
        KeyError
            If no key was found. Will change in the future to raise if not all
            keys were found.

        Returns
        -------
        scalar, DataFrame, or Series: indexed value(s).
        """
        # we assume that not com.is_bool_indexer(key), as that is
        #  handled before we get here.
        self._validate_key(key, axis)

        # A collection of keys
        keyarr, indexer = self._get_listlike_indexer(key, axis)
        return self.obj._reindex_with_indexers(
            {axis: [keyarr, indexer]}, copy=True, allow_dups=True
        )
