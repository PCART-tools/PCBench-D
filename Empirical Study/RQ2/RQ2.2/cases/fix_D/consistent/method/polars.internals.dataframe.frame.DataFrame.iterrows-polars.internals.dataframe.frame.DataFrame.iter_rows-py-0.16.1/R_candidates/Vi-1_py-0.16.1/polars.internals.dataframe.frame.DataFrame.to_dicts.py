    def to_dicts(self) -> list[dict[str, Any]]:
        """
        Convert every row to a dictionary.

        Note that this is slow.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3], "bar": [4, 5, 6]})
        >>> df.to_dicts()
        [{'foo': 1, 'bar': 4}, {'foo': 2, 'bar': 5}, {'foo': 3, 'bar': 6}]

        """
        return list(self.iter_rows(named=True))
