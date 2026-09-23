    def take(self, indices, allow_fill=False, fill_value=None, axis=None,
             **kwargs):
        """
        Take elements from the IntervalArray.

        Parameters
        ----------
        indices : sequence of integers
            Indices to be taken.

        allow_fill : bool, default False
            How to handle negative values in `indices`.

            * False: negative values in `indices` indicate positional indices
              from the right (the default). This is similar to
              :func:`numpy.take`.

            * True: negative values in `indices` indicate
              missing values. These values are set to `fill_value`. Any other
              other negative values raise a ``ValueError``.

        fill_value : Interval or NA, optional
            Fill value to use for NA-indices when `allow_fill` is True.
            This may be ``None``, in which case the default NA value for
            the type, ``self.dtype.na_value``, is used.

            For many ExtensionArrays, there will be two representations of
            `fill_value`: a user-facing "boxed" scalar, and a low-level
            physical NA value. `fill_value` should be the user-facing version,
            and the implementation should handle translating that to the
            physical version for processing the take if necessary.

        axis : any, default None
            Present for compat with IntervalIndex; does nothing.

        Returns
        -------
        IntervalArray

        Raises
        ------
        IndexError
            When the indices are out of bounds for the array.
        ValueError
            When `indices` contains negative values other than ``-1``
            and `allow_fill` is True.
        """
        from pandas.core.algorithms import take

        nv.validate_take(tuple(), kwargs)

        fill_left = fill_right = fill_value
        if allow_fill:
            if fill_value is None:
                fill_left = fill_right = self.left._na_value
            elif is_interval(fill_value):
                self._check_closed_matches(fill_value, name='fill_value')
                fill_left, fill_right = fill_value.left, fill_value.right
            elif not is_scalar(fill_value) and notna(fill_value):
                msg = ("'IntervalArray.fillna' only supports filling with a "
                       "'scalar pandas.Interval or NA'. Got a '{}' instead."
                       .format(type(fill_value).__name__))
                raise ValueError(msg)

        left_take = take(self.left, indices,
                         allow_fill=allow_fill, fill_value=fill_left)
        right_take = take(self.right, indices,
                          allow_fill=allow_fill, fill_value=fill_right)

        return self._shallow_copy(left_take, right_take)
