    def ends_with(self, suffix: IntoExpr) -> Series:
        r"""
        Check if string values end with a binary substring.

        Parameters
        ----------
        suffix
            Suffix substring.

        Examples
        --------
        >>> s = pl.Series("colors", [b"\x00\x00\x00", b"\xff\xff\x00", b"\x00\x00\xff"])
        >>> s.bin.ends_with(b"\x00")
        shape: (3,)
        Series: 'colors' [bool]
        [
            true
            true
            false
        ]
        """
