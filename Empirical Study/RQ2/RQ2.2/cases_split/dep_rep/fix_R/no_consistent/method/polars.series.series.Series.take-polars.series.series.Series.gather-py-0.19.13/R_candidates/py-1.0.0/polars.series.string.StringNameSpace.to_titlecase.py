    def to_titlecase(self) -> Series:
        """
        Modify the strings to their titlecase equivalent.

        Examples
        --------
        >>> s = pl.Series("sing", ["welcome to my world", "THERE'S NO TURNING BACK"])
        >>> s.str.to_titlecase()
        shape: (2,)
        Series: 'sing' [str]
        [
            "Welcome To My World"
            "There's No Turning Back"
        ]
        """
