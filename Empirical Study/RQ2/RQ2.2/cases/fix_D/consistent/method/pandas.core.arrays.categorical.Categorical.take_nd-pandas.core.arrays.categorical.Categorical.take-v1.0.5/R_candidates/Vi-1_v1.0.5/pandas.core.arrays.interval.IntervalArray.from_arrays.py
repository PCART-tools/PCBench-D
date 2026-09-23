    @classmethod
    @Appender(
        _interval_shared_docs["from_arrays"]
        % dict(
            klass="IntervalArray",
            examples=textwrap.dedent(
                """\
        >>> pd.arrays.IntervalArray.from_arrays([0, 1, 2], [1, 2, 3])
        <IntervalArray>
        [(0, 1], (1, 2], (2, 3]]
        Length: 3, closed: right, dtype: interval[int64]
        """
            ),
        )
    )
    def from_arrays(cls, left, right, closed="right", copy=False, dtype=None):
        left = maybe_convert_platform_interval(left)
        right = maybe_convert_platform_interval(right)

        return cls._simple_new(
            left, right, closed, copy=copy, dtype=dtype, verify_integrity=True
        )
