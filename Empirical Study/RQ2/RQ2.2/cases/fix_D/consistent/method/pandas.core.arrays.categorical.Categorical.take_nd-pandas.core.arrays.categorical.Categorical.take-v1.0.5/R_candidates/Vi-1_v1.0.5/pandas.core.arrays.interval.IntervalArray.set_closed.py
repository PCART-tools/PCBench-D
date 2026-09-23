    @Appender(
        _interval_shared_docs["set_closed"]
        % dict(
            klass="IntervalArray",
            examples=textwrap.dedent(
                """\
        Examples
        --------
        >>> index = pd.arrays.IntervalArray.from_breaks(range(4))
        >>> index
        <IntervalArray>
        [(0, 1], (1, 2], (2, 3]]
        Length: 3, closed: right, dtype: interval[int64]
        >>> index.set_closed('both')
        <IntervalArray>
        [[0, 1], [1, 2], [2, 3]]
        Length: 3, closed: both, dtype: interval[int64]
        """
            ),
        )
    )
    def set_closed(self, closed):
        if closed not in _VALID_CLOSED:
            msg = f"invalid option for 'closed': {closed}"
            raise ValueError(msg)

        return self._shallow_copy(closed=closed)
