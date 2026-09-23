    def to_local(self) -> Series:
        """
        Convert a categorical column to its local representation.

        This may change the underlying physical representation of the column.

        See the documentation of :func:`StringCache` for more information on the
        difference between local and global categoricals.

        Examples
        --------
        Compare the global and local representations of a categorical.

        >>> with pl.StringCache():
        ...     _ = pl.Series("x", ["a", "b", "a"], dtype=pl.Categorical)
        ...     s = pl.Series("y", ["c", "b", "d"], dtype=pl.Categorical)
        >>> s.to_physical()
        shape: (3,)
        Series: 'y' [u32]
        [
                2
                1
                3
        ]
        >>> s.cat.to_local().to_physical()
        shape: (3,)
        Series: 'y' [u32]
        [
                0
                1
                2
        ]
        """
        return wrap_s(self._s.cat_to_local())
