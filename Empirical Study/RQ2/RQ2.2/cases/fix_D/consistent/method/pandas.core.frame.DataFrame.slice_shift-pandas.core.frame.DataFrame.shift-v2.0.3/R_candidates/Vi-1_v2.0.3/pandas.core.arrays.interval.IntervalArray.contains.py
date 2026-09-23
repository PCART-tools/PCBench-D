    @Appender(
        _interval_shared_docs["contains"]
        % {
            "klass": "IntervalArray",
            "examples": textwrap.dedent(
                """\
        >>> intervals = pd.arrays.IntervalArray.from_tuples([(0, 1), (1, 3), (2, 4)])
        >>> intervals
        <IntervalArray>
        [(0, 1], (1, 3], (2, 4]]
        Length: 3, dtype: interval[int64, right]
        """
            ),
        }
    )
    def contains(self, other):
        if isinstance(other, Interval):
            raise NotImplementedError("contains not implemented for two intervals")

        return (self._left < other if self.open_left else self._left <= other) & (
            other < self._right if self.open_right else other <= self._right
        )
