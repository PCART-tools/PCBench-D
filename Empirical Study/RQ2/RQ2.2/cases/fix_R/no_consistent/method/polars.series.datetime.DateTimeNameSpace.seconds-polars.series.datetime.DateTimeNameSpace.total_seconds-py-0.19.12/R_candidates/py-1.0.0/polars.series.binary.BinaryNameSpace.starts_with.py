    def starts_with(self, prefix: IntoExpr) -> Series:
        r"""
        Check if values start with a binary substring.

        Parameters
        ----------
        prefix
            Prefix substring.

        Examples
        --------
        >>> s = pl.Series("colors", [b"\x00\x00\x00", b"\xff\xff\x00", b"\x00\x00\xff"])
        >>> s.bin.starts_with(b"\x00")
        shape: (3,)
        Series: 'colors' [bool]
        [
            true
            false
            true
        ]
        """
