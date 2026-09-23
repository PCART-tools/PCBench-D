    def field(self, name: str) -> Series:
        """
        Retrieve one of the fields of this `Struct` as a new Series.

        Parameters
        ----------
        name
            Name of the field.

        Examples
        --------
        >>> s = pl.Series([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        >>> s.struct.field("a")
        shape: (2,)
        Series: 'a' [i64]
        [
            1
            3
        ]
        """
