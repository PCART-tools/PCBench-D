    def to_pandas(
        self, *args: Any, date_as_object: bool = False, **kwargs: Any
    ) -> pd.DataFrame:
        """
        Cast to a pandas DataFrame.

        This requires that :mod:`pandas` and :mod:`pyarrow` are installed.
        This operation clones data.

        Parameters
        ----------
        args
            Arguments will be sent to :meth:`pyarrow.Table.to_pandas`.
        date_as_object
            Cast dates to objects. If ``False``, convert to ``datetime64[ns]`` dtype.
        kwargs
            Arguments will be sent to :meth:`pyarrow.Table.to_pandas`.

        Returns
        -------
        :class:`pandas.DataFrame`

        Examples
        --------
        >>> import pandas
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> pandas_df = df.to_pandas()
        >>> type(pandas_df)
        <class 'pandas.core.frame.DataFrame'>

        """
        record_batches = self._df.to_pandas()
        tbl = pa.Table.from_batches(record_batches)
        return tbl.to_pandas(*args, date_as_object=date_as_object, **kwargs)
