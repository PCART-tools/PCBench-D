    @Appender(
        _interval_shared_docs["to_tuples"]
        % {
            "return_type": (
                "ndarray (if self is IntervalArray) or Index (if self is IntervalIndex)"
            ),
            "examples": textwrap.dedent(
                """\

         Examples
         --------
         For :class:`pandas.IntervalArray`:

         >>> idx = pd.arrays.IntervalArray.from_tuples([(0, 1), (1, 2)])
         >>> idx
         <IntervalArray>
         [(0, 1], (1, 2]]
         Length: 2, dtype: interval[int64, right]
         >>> idx.to_tuples()
         array([(0, 1), (1, 2)], dtype=object)

         For :class:`pandas.IntervalIndex`:

         >>> idx = pd.interval_range(start=0, end=2)
         >>> idx
         IntervalIndex([(0, 1], (1, 2]], dtype='interval[int64, right]')
         >>> idx.to_tuples()
         Index([(0, 1), (1, 2)], dtype='object')
         """
            ),
        }
    )
    def to_tuples(self, na_tuple: bool = True) -> np.ndarray:
        tuples = com.asarray_tuplesafe(zip(self._left, self._right))
        if not na_tuple:
            # GH 18756
            tuples = np.where(~self.isna(), tuples, np.nan)
        return tuples
