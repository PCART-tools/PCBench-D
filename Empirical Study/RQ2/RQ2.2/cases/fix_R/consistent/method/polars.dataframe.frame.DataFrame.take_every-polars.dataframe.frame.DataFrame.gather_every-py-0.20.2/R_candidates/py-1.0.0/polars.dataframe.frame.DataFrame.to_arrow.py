    def to_arrow(self, *, future: bool = False) -> pa.Table:
        """
        Collect the underlying arrow arrays in an Arrow Table.

        This operation is mostly zero copy.

        Data types that do copy:
            - CategoricalType

        Parameters
        ----------
        future
            Setting this to `True` will write Polars' internal data structures that
            might not be available by other Arrow implementations.

            .. warning::
                This functionality is considered **unstable**. It may be changed
                at any point without it being considered a breaking change.

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

        if future:
            issue_unstable_warning(
                "The `future` parameter of `DataFrame.to_arrow` is considered unstable."
            )

        record_batches = self._df.to_arrow(future)
        return pa.Table.from_batches(record_batches)
