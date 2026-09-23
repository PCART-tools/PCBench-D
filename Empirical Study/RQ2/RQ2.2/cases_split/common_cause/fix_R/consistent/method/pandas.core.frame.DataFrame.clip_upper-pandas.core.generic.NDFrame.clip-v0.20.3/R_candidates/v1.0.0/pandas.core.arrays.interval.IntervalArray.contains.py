    @Appender(
        _interval_shared_docs["contains"]
        % dict(
            klass="IntervalArray",
            examples=textwrap.dedent(
                """\
        >>> intervals = pd.arrays.IntervalArray.from_tuples([(0, 1), (1, 3), (2, 4)])
        >>> intervals
        <IntervalArray>
        [(0, 1], (1, 3], (2, 4]]
        Length: 3, closed: right, dtype: interval[int64]
        """
            ),
        )
    )
    def contains(self, other):
        if isinstance(other, Interval):
            raise NotImplementedError("contains not implemented for two intervals")

        return (self.left < other if self.open_left else self.left <= other) & (
            other < self.right if self.open_right else other <= self.right
        )
