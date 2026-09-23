    def to_dicts(self) -> list[dict[str, Any]]:
        """
        Convert every row to a dictionary of Python-native values.

        Notes
        -----
        If you have `ns`-precision temporal values you should be aware that Python
        natively only supports up to `μs`-precision; `ns`-precision values will be
        truncated to microseconds on conversion to Python. If this matters to your
        use-case you should export to a different format (such as Arrow or NumPy).

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3], "bar": [4, 5, 6]})
        >>> df.to_dicts()
        [{'foo': 1, 'bar': 4}, {'foo': 2, 'bar': 5}, {'foo': 3, 'bar': 6}]
        """
        return self.rows(named=True)
