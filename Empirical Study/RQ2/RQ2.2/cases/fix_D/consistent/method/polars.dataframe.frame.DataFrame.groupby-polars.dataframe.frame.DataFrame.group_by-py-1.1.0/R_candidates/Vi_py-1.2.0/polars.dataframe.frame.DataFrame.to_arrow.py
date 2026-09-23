    @deprecate_renamed_parameter("future", "compat_level", version="1.1")
    def to_arrow(self, *, compat_level: CompatLevel | None = None) -> pa.Table:
        """
        Collect the underlying arrow arrays in an Arrow Table.

        This operation is mostly zero copy.

        Data types that do copy:
            - CategoricalType

        Parameters
        ----------
        compat_level
            Use a specific compatibility level
            when exporting Polars' internal data structures.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"foo": [1, 2, 3, 4, 5, 6], "bar": ["a", "b", "c", "d", "e", "f"]}
        ... )
        >>> df.to_arrow()
        pyarrow.Table
        foo: int64
        bar: large_string
        ----
        foo: [[1,2,3,4,5,6]]
        bar: [["a","b","c","d","e","f"]]
        """
        if not self.width:  # 0x0 dataframe, cannot infer schema from batches
            return pa.table({})

        if compat_level is None:
            compat_level = False  # type: ignore[assignment]
        elif isinstance(compat_level, CompatLevel):
            compat_level = compat_level._version  # type: ignore[attr-defined]

        record_batches = self._df.to_arrow(compat_level)
        return pa.Table.from_batches(record_batches)
