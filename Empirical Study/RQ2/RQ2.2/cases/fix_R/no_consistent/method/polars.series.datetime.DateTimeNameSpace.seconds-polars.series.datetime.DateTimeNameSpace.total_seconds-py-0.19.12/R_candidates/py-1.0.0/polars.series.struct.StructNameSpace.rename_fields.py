    def rename_fields(self, names: Sequence[str]) -> Series:
        """
        Rename the fields of the struct.

        Parameters
        ----------
        names
            New names in the order of the struct's fields.

        Examples
        --------
        >>> s = pl.Series([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        >>> s.struct.fields
        ['a', 'b']
        >>> s = s.struct.rename_fields(["c", "d"])
        >>> s.struct.fields
        ['c', 'd']
        """
