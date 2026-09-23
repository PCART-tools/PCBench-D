    def reverse(self) -> Series:
        """
        Returns string values in reversed order.

        Examples
        --------
        >>> s = pl.Series("text", ["foo", "bar", "man\u0303ana"])
        >>> s.str.reverse()
        shape: (3,)
        Series: 'text' [str]
        [
            "oof"
            "rab"
            "anañam"
        ]
        """
