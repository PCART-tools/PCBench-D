    def to_integer(self, *, base: int = 10, strict: bool = True) -> Series:
        """
        Convert an String column into an Int64 column with base radix.

        Parameters
        ----------
        base
            Positive integer which is the base of the string we are parsing.
            Default: 10.
        strict
            Bool, Default=True will raise any ParseError or overflow as ComputeError.
            False silently convert to Null.

        Returns
        -------
        Series
            Series of data type :class:`Int64`.

        Examples
        --------
        >>> s = pl.Series("bin", ["110", "101", "010", "invalid"])
        >>> s.str.to_integer(base=2, strict=False)
        shape: (4,)
        Series: 'bin' [i64]
        [
                6
                5
                2
                null
        ]

        >>> s = pl.Series("hex", ["fa1e", "ff00", "cafe", None])
        >>> s.str.to_integer(base=16)
        shape: (4,)
        Series: 'hex' [i64]
        [
                64030
                65280
                51966
                null
        ]

        """
