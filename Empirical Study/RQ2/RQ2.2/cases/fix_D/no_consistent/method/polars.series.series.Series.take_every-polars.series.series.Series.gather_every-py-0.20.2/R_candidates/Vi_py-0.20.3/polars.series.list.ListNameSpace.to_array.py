    def to_array(self, width: int) -> Series:
        """
        Convert a List column into an Array column with the same inner data type.

        Parameters
        ----------
        width
            Width of the resulting Array column.

        Returns
        -------
        Series
            Series of data type :class:`Array`.

        Examples
        --------
        >>> s = pl.Series([[1, 2], [3, 4]], dtype=pl.List(pl.Int8))
        >>> s.list.to_array(2)
        shape: (2,)
        Series: '' [array[i8, 2]]
        [
                [1, 2]
                [3, 4]
        ]

        """
