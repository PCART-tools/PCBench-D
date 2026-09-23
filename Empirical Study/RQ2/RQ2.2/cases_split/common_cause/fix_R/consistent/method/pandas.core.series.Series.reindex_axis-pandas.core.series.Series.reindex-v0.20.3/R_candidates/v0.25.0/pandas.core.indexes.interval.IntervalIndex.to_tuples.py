    @Appender(
        _interval_shared_docs["to_tuples"]
        % dict(
            return_type="Index",
            examples="""
        Examples
        --------
        >>> idx = pd.IntervalIndex.from_arrays([0, np.nan, 2], [1, np.nan, 3])
        >>> idx.to_tuples()
        Index([(0.0, 1.0), (nan, nan), (2.0, 3.0)], dtype='object')
        >>> idx.to_tuples(na_tuple=False)
        Index([(0.0, 1.0), nan, (2.0, 3.0)], dtype='object')""",
        )
    )
    def to_tuples(self, na_tuple=True):
        tuples = self._data.to_tuples(na_tuple=na_tuple)
        return Index(tuples)
