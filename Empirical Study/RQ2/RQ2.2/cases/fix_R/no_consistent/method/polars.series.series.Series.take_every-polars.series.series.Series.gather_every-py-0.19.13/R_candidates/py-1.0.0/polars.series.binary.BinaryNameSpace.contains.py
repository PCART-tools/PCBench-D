    def contains(self, literal: IntoExpr) -> Series:
        r"""
        Check if binaries in Series contain a binary substring.

        Parameters
        ----------
        literal
            The binary substring to look for

        Returns
        -------
        Series
            Series of data type :class:`Boolean`.

        Examples
        --------
        >>> s = pl.Series("colors", [b"\x00\x00\x00", b"\xff\xff\x00", b"\x00\x00\xff"])
        >>> s.bin.contains(b"\xff")
        shape: (3,)
        Series: 'colors' [bool]
        [
            false
            true
            true
        ]
        """
