    @classmethod
    @Appender(
        _interval_shared_docs["from_tuples"]
        % dict(
            klass="IntervalArray",
            examples=textwrap.dedent(
                """\
        Examples
        --------
        >>> pd.arrays.IntervalArray.from_tuples([(0, 1), (1, 2)])
        <IntervalArray>
        [(0, 1], (1, 2]]
        Length: 2, closed: right, dtype: interval[int64]
        """
            ),
        )
    )
    def from_tuples(cls, data, closed="right", copy=False, dtype=None):
        if len(data):
            left, right = [], []
        else:
            # ensure that empty data keeps input dtype
            left = right = data

        for d in data:
            if isna(d):
                lhs = rhs = np.nan
            else:
                name = cls.__name__
                try:
                    # need list of length 2 tuples, e.g. [(0, 1), (1, 2), ...]
                    lhs, rhs = d
                except ValueError:
                    msg = f"{name}.from_tuples requires tuples of length 2, got {d}"
                    raise ValueError(msg)
                except TypeError:
                    msg = f"{name}.from_tuples received an invalid item, {d}"
                    raise TypeError(msg)
            left.append(lhs)
            right.append(rhs)

        return cls.from_arrays(left, right, closed, copy=False, dtype=dtype)
