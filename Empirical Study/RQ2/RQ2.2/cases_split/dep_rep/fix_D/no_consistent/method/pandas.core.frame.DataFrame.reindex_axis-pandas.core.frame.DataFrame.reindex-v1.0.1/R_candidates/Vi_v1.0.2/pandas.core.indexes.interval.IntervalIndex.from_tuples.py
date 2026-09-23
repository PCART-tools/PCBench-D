    @classmethod
    @Appender(
        _interval_shared_docs["from_tuples"]
        % dict(
            klass="IntervalIndex",
            examples=textwrap.dedent(
                """\
        Examples
        --------
        >>> pd.IntervalIndex.from_tuples([(0, 1), (1, 2)])
        IntervalIndex([(0, 1], (1, 2]],
                       closed='right',
                       dtype='interval[int64]')
        """
            ),
        )
    )
    def from_tuples(
        cls, data, closed: str = "right", name=None, copy: bool = False, dtype=None
    ):
        with rewrite_exception("IntervalArray", cls.__name__):
            arr = IntervalArray.from_tuples(data, closed=closed, copy=copy, dtype=dtype)
        return cls._simple_new(arr, name=name)
