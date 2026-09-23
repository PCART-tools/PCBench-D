    def to_dicts(self) -> list[dict[str, Any]]:
        """
        Convert every row to a dictionary of python-native values.

        Notes
        -----
        If you have ``ns``-precision temporal values you should be aware that python
        natively only supports up to ``us``-precision; if this matters you should export
        to a different format.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3], "bar": [4, 5, 6]})
        >>> df.to_dicts()
        [{'foo': 1, 'bar': 4}, {'foo': 2, 'bar': 5}, {'foo': 3, 'bar': 6}]

        """
        return list(self.iter_rows(named=True))
