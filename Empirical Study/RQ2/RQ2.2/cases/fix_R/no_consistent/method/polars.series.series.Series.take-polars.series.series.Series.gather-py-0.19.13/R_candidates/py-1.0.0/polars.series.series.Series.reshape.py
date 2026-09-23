    def reshape(self, dimensions: tuple[int, ...]) -> Series:
        """
        Reshape this Series to a flat Series or an Array Series.

        Parameters
        ----------
        dimensions
            Tuple of the dimension sizes. If a -1 is used in any of the dimensions, that
            dimension is inferred.

        Returns
        -------
        Series
            If a single dimension is given, results in a Series of the original
            data type.
            If a multiple dimensions are given, results in a Series of data type
            :class:`Array` with shape `dimensions`.

        See Also
        --------
        Series.list.explode : Explode a list column.

        Examples
        --------
        >>> s = pl.Series("foo", [1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> square = s.reshape((3, 3))
        >>> square
        shape: (3,)
        Series: 'foo' [array[i64, 3]]
        [
                [1, 2, 3]
                [4, 5, 6]
                [7, 8, 9]
        ]
        >>> square.reshape((9,))
        shape: (9,)
        Series: 'foo' [i64]
        [
                1
                2
                3
                4
                5
                6
                7
                8
                9
        ]
        """
        return self._from_pyseries(self._s.reshape(dimensions))
