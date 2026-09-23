    def iter_slices(self, n_rows: int = 10_000) -> Iterator[DataFrame]:
        r"""
        Returns a non-copying iterator of slices over the underlying DataFrame.

        Parameters
        ----------
        n_rows
            Determines the number of rows contained in each DataFrame slice.

        Examples
        --------
        >>> from datetime import date
        >>> df = pl.DataFrame(
        ...     data={
        ...         "a": range(17_500),
        ...         "b": date(2023, 1, 1),
        ...         "c": "klmnoopqrstuvwxyz",
        ...     },
        ...     schema_overrides={"a": pl.Int32},
        ... )
        >>> for idx, frame in enumerate(df.iter_slices()):
        ...     print(f"{type(frame).__name__}:[{idx}]:{len(frame)}")
        DataFrame:[0]:10000
        DataFrame:[1]:7500

        Using `iter_slices` is an efficient way to chunk-iterate over DataFrames and
        any supported frame export/conversion types; for example, as RecordBatches:

        >>> for frame in df.iter_slices(n_rows=15_000):
        ...     record_batch = frame.to_arrow().to_batches()[0]
        ...     print(f"{record_batch.schema}\n<< {len(record_batch)}")
        a: int32
        b: date32[day]
        c: large_string
        << 15000
        a: int32
        b: date32[day]
        c: large_string
        << 2500

        See Also
        --------
        iter_rows : Row iterator over frame data (does not materialise all rows).
        partition_by : Split into multiple DataFrames, partitioned by groups.

        """
        for offset in range(0, self.height, n_rows):
            yield self.slice(offset, n_rows)
