    @doc(
        Series.diff,
        klass="DataFrame",
        extra_params="axis : {0 or 'index', 1 or 'columns'}, default 0\n    "
        "Take difference over rows (0) or columns (1).\n",
        other_klass="Series",
        examples=dedent(
            """
        Difference with previous row

        >>> df = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6],
        ...                    'b': [1, 1, 2, 3, 5, 8],
        ...                    'c': [1, 4, 9, 16, 25, 36]})
        >>> df
           a  b   c
        0  1  1   1
        1  2  1   4
        2  3  2   9
        3  4  3  16
        4  5  5  25
        5  6  8  36

        >>> df.diff()
             a    b     c
        0  NaN  NaN   NaN
        1  1.0  0.0   3.0
        2  1.0  1.0   5.0
        3  1.0  1.0   7.0
        4  1.0  2.0   9.0
        5  1.0  3.0  11.0

        Difference with previous column

        >>> df.diff(axis=1)
            a  b   c
        0 NaN  0   0
        1 NaN -1   3
        2 NaN -1   7
        3 NaN -1  13
        4 NaN  0  20
        5 NaN  2  28

        Difference with 3rd previous row

        >>> df.diff(periods=3)
             a    b     c
        0  NaN  NaN   NaN
        1  NaN  NaN   NaN
        2  NaN  NaN   NaN
        3  3.0  2.0  15.0
        4  3.0  4.0  21.0
        5  3.0  6.0  27.0

        Difference with following row

        >>> df.diff(periods=-1)
             a    b     c
        0 -1.0  0.0  -3.0
        1 -1.0 -1.0  -5.0
        2 -1.0 -1.0  -7.0
        3 -1.0 -2.0  -9.0
        4 -1.0 -3.0 -11.0
        5  NaN  NaN   NaN

        Overflow in input dtype

        >>> df = pd.DataFrame({'a': [1, 0]}, dtype=np.uint8)
        >>> df.diff()
               a
        0    NaN
        1  255.0"""
        ),
    )
    def diff(self, periods: int = 1, axis: Axis = 0) -> DataFrame:
        if not lib.is_integer(periods):
            if not (
                is_float(periods)
                # error: "int" has no attribute "is_integer"
                and periods.is_integer()  # type: ignore[attr-defined]
            ):
                raise ValueError("periods must be an integer")
            periods = int(periods)

        axis = self._get_axis_number(axis)
        if axis == 1:
            if periods != 0:
                # in the periods == 0 case, this is equivalent diff of 0 periods
                #  along axis=0, and the Manager method may be somewhat more
                #  performant, so we dispatch in that case.
                return self - self.shift(periods, axis=axis)
            # With periods=0 this is equivalent to a diff with axis=0
            axis = 0

        new_data = self._mgr.diff(n=periods, axis=axis)
        return self._constructor(new_data).__finalize__(self, "diff")
