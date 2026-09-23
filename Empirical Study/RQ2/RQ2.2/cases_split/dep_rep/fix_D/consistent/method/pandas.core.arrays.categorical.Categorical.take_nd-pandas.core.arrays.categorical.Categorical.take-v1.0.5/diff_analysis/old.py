    def take(self, indexer, allow_fill: bool = False, fill_value=None):
        """
        Take elements from the Categorical.

        Parameters
        ----------
        indexer : sequence of int
            The indices in `self` to take. The meaning of negative values in
            `indexer` depends on the value of `allow_fill`.
        allow_fill : bool, default False
            How to handle negative values in `indexer`.

            * False: negative values in `indices` indicate positional indices
              from the right. This is similar to
              :func:`numpy.take`.

            * True: negative values in `indices` indicate missing values
              (the default). These values are set to `fill_value`. Any other
              other negative values raise a ``ValueError``.

            .. versionchanged:: 1.0.0

               Default value changed from ``True`` to ``False``.

        fill_value : object
            The value to use for `indices` that are missing (-1), when
            ``allow_fill=True``. This should be the category, i.e. a value
            in ``self.categories``, not a code.

        Returns
        -------
        Categorical
            This Categorical will have the same categories and ordered as
            `self`.

        See Also
        --------
        Series.take : Similar method for Series.
        numpy.ndarray.take : Similar method for NumPy arrays.

        Examples
        --------
        >>> cat = pd.Categorical(['a', 'a', 'b'])
        >>> cat
        [a, a, b]
        Categories (2, object): [a, b]

        Specify ``allow_fill==False`` to have negative indices mean indexing
        from the right.

        >>> cat.take([0, -1, -2], allow_fill=False)
        [a, b, a]
        Categories (2, object): [a, b]

        With ``allow_fill=True``, indices equal to ``-1`` mean "missing"
        values that should be filled with the `fill_value`, which is
        ``np.nan`` by default.

        >>> cat.take([0, -1, -1], allow_fill=True)
        [a, NaN, NaN]
        Categories (2, object): [a, b]

        The fill value can be specified.

        >>> cat.take([0, -1, -1], allow_fill=True, fill_value='a')
        [a, a, a]
        Categories (3, object): [a, b]

        Specifying a fill value that's not in ``self.categories``
        will raise a ``TypeError``.
        """
        indexer = np.asarray(indexer, dtype=np.intp)

        dtype = self.dtype

        if isna(fill_value):
            fill_value = -1
        elif allow_fill:
            # convert user-provided `fill_value` to codes
            if fill_value in self.categories:
                fill_value = self.categories.get_loc(fill_value)
            else:
                msg = (
                    f"'fill_value' ('{fill_value}') is not in this "
                    "Categorical's categories."
                )
                raise TypeError(msg)

        codes = take(self._codes, indexer, allow_fill=allow_fill, fill_value=fill_value)
        result = type(self).from_codes(codes, dtype=dtype)
        return result
