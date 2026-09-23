    def reshape(
        self, dimensions: tuple[int, ...], nested_type: type[Array] | type[List] = List
    ) -> Series:
        """
        Reshape this Series to a flat Series or a Series of Lists.

        Parameters
        ----------
        dimensions
            Tuple of the dimension sizes. If a -1 is used in any of the dimensions, that
            dimension is inferred.
        nested_type
            The nested data type to create. List only supports 2 dimension,
            whereas Array supports an arbitrary number of dimensions.

        Returns
        -------
        Series
            If a single dimension is given, results in a Series of the original
            data type.
            If a multiple dimensions are given, results in a Series of data type
            :class:`List` with shape (rows, cols)
            or :class:`Array` with shape `dimensions`.

        See Also
        --------
        Series.list.explode : Explode a list column.

        Examples
        --------
        >>> s = pl.Series("foo", [1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> s.reshape((3, 3))
        shape: (3,)
        Series: 'foo' [list[i64]]
        [
                [1, 2, 3]
                [4, 5, 6]
                [7, 8, 9]
        ]
        """
        is_list = nested_type == List
        return self._from_pyseries(self._s.reshape(dimensions, is_list))
