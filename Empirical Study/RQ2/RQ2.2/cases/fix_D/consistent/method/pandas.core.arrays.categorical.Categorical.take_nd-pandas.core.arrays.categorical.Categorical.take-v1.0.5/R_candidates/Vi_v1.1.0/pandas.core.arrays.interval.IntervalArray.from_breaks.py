    @classmethod
    @Appender(
        _interval_shared_docs["from_breaks"]
        % dict(
            klass="IntervalArray",
            examples=textwrap.dedent(
                """\
        Examples
        --------
        >>> pd.arrays.IntervalArray.from_breaks([0, 1, 2, 3])
        <IntervalArray>
        [(0, 1], (1, 2], (2, 3]]
        Length: 3, closed: right, dtype: interval[int64]
        """
            ),
        )
    )
    def from_breaks(cls, breaks, closed="right", copy=False, dtype=None):
        breaks = maybe_convert_platform_interval(breaks)

        return cls.from_arrays(breaks[:-1], breaks[1:], closed, copy=copy, dtype=dtype)
