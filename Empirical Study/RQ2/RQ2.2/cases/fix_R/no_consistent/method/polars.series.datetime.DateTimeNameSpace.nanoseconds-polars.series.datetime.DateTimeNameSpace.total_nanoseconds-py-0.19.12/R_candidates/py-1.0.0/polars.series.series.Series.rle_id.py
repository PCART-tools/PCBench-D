    def rle_id(self) -> Series:
        """
        Get a distinct integer ID for each run of identical values.

        The ID starts at 0 and increases by one each time the value of the column
        changes.

        Returns
        -------
        Series
            Series of data type `UInt32`.

        See Also
        --------
        rle

        Notes
        -----
        This functionality is especially useful for defining a new group for every time
        a column's value changes, rather than for every distinct value of that column.

        Examples
        --------
        >>> s = pl.Series("s", [1, 1, 2, 1, None, 1, 3, 3])
        >>> s.rle_id()
        shape: (8,)
        Series: 's' [u32]
        [
            0
            0
            1
            2
            3
            4
            5
            5
        ]
        """
