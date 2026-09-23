    @classmethod
    @Appender(
        _interval_shared_docs["from_breaks"]
        % {
            "klass": "IntervalIndex",
            "examples": textwrap.dedent(
                """\
        Examples
        --------
        >>> pd.IntervalIndex.from_breaks([0, 1, 2, 3])
        IntervalIndex([(0, 1], (1, 2], (2, 3]],
                      closed='right',
                      dtype='interval[int64]')
        """
            ),
        }
    )
    def from_breaks(
        cls, breaks, closed: str = "right", name=None, copy: bool = False, dtype=None
    ):
        with rewrite_exception("IntervalArray", cls.__name__):
            array = IntervalArray.from_breaks(
                breaks, closed=closed, copy=copy, dtype=dtype
            )
        return cls._simple_new(array, name=name)
