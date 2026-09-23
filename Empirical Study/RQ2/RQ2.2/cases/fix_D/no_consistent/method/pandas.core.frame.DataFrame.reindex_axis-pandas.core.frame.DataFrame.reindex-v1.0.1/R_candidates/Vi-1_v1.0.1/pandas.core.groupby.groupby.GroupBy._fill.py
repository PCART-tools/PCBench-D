    def _fill(self, direction, limit=None):
        """
        Shared function for `pad` and `backfill` to call Cython method.

        Parameters
        ----------
        direction : {'ffill', 'bfill'}
            Direction passed to underlying Cython function. `bfill` will cause
            values to be filled backwards. `ffill` and any other values will
            default to a forward fill
        limit : int, default None
            Maximum number of consecutive values to fill. If `None`, this
            method will convert to -1 prior to passing to Cython

        Returns
        -------
        `Series` or `DataFrame` with filled values

        See Also
        --------
        pad
        backfill
        """
        # Need int value for Cython
        if limit is None:
            limit = -1

        return self._get_cythonized_result(
            "group_fillna_indexer",
            needs_mask=True,
            cython_dtype=np.dtype(np.int64),
            result_is_index=True,
            direction=direction,
            limit=limit,
        )
