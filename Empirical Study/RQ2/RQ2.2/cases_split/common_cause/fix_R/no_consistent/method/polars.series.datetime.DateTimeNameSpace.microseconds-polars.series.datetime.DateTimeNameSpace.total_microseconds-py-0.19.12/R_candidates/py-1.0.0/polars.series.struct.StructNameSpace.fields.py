    @property
    def fields(self) -> list[str]:
        """
        Get the names of the fields.

        Examples
        --------
        >>> s = pl.Series([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        >>> s.struct.fields
        ['a', 'b']
        """
        if getattr(self, "_s", None) is None:
            return []
        return self._s.struct_fields()
