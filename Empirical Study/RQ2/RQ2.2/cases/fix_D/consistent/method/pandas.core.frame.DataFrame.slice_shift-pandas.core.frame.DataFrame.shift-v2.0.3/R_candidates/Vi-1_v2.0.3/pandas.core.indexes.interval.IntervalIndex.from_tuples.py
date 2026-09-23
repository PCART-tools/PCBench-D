    @classmethod
    @Appender(
        _interval_shared_docs["from_tuples"]
        % {
            "klass": "IntervalIndex",
            "name": textwrap.dedent(
                """
             name : str, optional
                  Name of the resulting IntervalIndex."""
            ),
            "examples": textwrap.dedent(
                """\
        Examples
        --------
        >>> pd.IntervalIndex.from_tuples([(0, 1), (1, 2)])
        IntervalIndex([(0, 1], (1, 2]],
                       dtype='interval[int64, right]')
        """
            ),
        }
    )
    def from_tuples(
        cls,
        data,
        closed: IntervalClosedType = "right",
        name: Hashable = None,
        copy: bool = False,
        dtype: Dtype | None = None,
    ) -> IntervalIndex:
        with rewrite_exception("IntervalArray", cls.__name__):
            arr = IntervalArray.from_tuples(data, closed=closed, copy=copy, dtype=dtype)
        return cls._simple_new(arr, name=name)
