    def _get_listlike_indexer(self, key, axis: int, raise_missing: bool = False):
        """
        Transform a list-like of keys into a new index and an indexer.

        Parameters
        ----------
        key : list-like
            Target labels
        axis: int
            Dimension on which the indexing is being made
        raise_missing: bool
            Whether to raise a KeyError if some labels are not found. Will be
            removed in the future, and then this method will always behave as
            if raise_missing=True.

        Raises
        ------
        KeyError
            If at least one key was requested but none was found, and
            raise_missing=True.

        Returns
        -------
        keyarr: Index
            New index (coinciding with 'key' if the axis is unique)
        values : array-like
            An indexer for the return object; -1 denotes keys not found
        """
        o = self.obj
        ax = o._get_axis(axis)

        # Have the index compute an indexer or return None
        # if it cannot handle:
        indexer, keyarr = ax._convert_listlike_indexer(key, kind=self.name)
        # We only act on all found values:
        if indexer is not None and (indexer != -1).all():
            self._validate_read_indexer(key, indexer, axis, raise_missing=raise_missing)
            return ax[indexer], indexer

        if ax.is_unique and not getattr(ax, "is_overlapping", False):
            # If we are trying to get actual keys from empty Series, we
            # patiently wait for a KeyError later on - otherwise, convert
            if len(ax) or not len(key):
                key = self._convert_for_reindex(key, axis)
            indexer = ax.get_indexer_for(key)
            keyarr = ax.reindex(keyarr)[0]
        else:
            keyarr, indexer, new_indexer = ax._reindex_non_unique(keyarr)

        self._validate_read_indexer(
            keyarr, indexer, o._get_axis_number(axis), raise_missing=raise_missing
        )
        return keyarr, indexer
