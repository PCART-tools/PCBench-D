    def alias(self, name: str) -> Series:
        """
        Rename the series.

        Parameters
        ----------
        name
            The new name.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.alias("b")
        shape: (3,)
        Series: 'b' [i64]
        [
                1
                2
                3
        ]
        """
        s = self.clone()
        s._s.rename(name)
        return s
