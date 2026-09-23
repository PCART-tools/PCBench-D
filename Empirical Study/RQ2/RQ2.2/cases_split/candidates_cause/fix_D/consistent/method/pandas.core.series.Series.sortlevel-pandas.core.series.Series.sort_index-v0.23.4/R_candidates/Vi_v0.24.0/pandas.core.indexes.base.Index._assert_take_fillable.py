    def _assert_take_fillable(self, values, indices, allow_fill=True,
                              fill_value=None, na_value=np.nan):
        """
        Internal method to handle NA filling of take.
        """
        indices = ensure_platform_int(indices)

        # only fill if we are passing a non-None fill_value
        if allow_fill and fill_value is not None:
            if (indices < -1).any():
                msg = ('When allow_fill=True and fill_value is not None, '
                       'all indices must be >= -1')
                raise ValueError(msg)
            taken = algos.take(values,
                               indices,
                               allow_fill=allow_fill,
                               fill_value=na_value)
        else:
            taken = values.take(indices)
        return taken
