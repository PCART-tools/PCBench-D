    @classmethod
    @Appender(
        _interval_shared_docs["from_arrays"]
        % {
            "klass": "IntervalArray",
            "examples": textwrap.dedent(
                """\
        >>> pd.arrays.IntervalArray.from_arrays([0, 1, 2], [1, 2, 3])
        <IntervalArray>
        [(0, 1], (1, 2], (2, 3]]
        Length: 3, dtype: interval[int64, right]
        """
            ),
        }
    )
    def from_arrays(
        cls: type[IntervalArrayT],
        left,
        right,
        closed="right",
        copy: bool = False,
        dtype: Dtype | None = None,
    ) -> IntervalArrayT:
        left = _maybe_convert_platform_interval(left)
        right = _maybe_convert_platform_interval(right)

        return cls._simple_new(
            left, right, closed, copy=copy, dtype=dtype, verify_integrity=True
        )
