    def _init_dict(self, data, index=None, dtype=None):
        """
        Derive the "_data" and "index" attributes of a new Series from a
        dictionary input.

        Parameters
        ----------
        data : dict or dict-like
            Data used to populate the new Series.
        index : Index or index-like, default None
            Index for the new Series: if None, use dict keys.
        dtype : dtype, default None
            The dtype for the new Series: if None, infer from data.

        Returns
        -------
        _data : BlockManager for the new Series
        index : index for the new Series
        """
        # Looking for NaN in dict doesn't work ({np.nan : 1}[float('nan')]
        # raises KeyError), so we iterate the entire dict, and align
        if data:
            keys, values = zip(*data.items())
            values = list(values)
        elif index is not None:
            # fastpath for Series(data=None). Just use broadcasting a scalar
            # instead of reindexing.
            values = na_value_for_dtype(dtype)
            keys = index
        else:
            keys, values = [], []

        # Input is now list-like, so rely on "standard" construction:

        # TODO: passing np.float64 to not break anything yet. See GH-17261
        s = create_series_with_explicit_dtype(
            values, index=keys, dtype=dtype, dtype_if_empty=np.float64
        )

        # Now we just make sure the order is respected, if any
        if data and index is not None:
            s = s.reindex(index, copy=False)
        return s._data, s.index
