    def to_arrow(self) -> pa.Array:
        """
        Get the underlying Arrow Array.

        If the Series contains only a single chunk this operation is zero copy.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s = s.to_arrow()
        >>> s  # doctest: +ELLIPSIS
        <pyarrow.lib.Int64Array object at ...>
        [
          1,
          2,
          3
        ]

        """
        return self._s.to_arrow()
