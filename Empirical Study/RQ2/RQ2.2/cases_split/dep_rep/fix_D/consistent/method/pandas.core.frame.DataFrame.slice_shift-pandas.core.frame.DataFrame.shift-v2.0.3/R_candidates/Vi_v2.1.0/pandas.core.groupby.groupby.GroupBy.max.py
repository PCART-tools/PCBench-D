    @final
    @doc(
        _groupby_agg_method_engine_template,
        fname="max",
        no=False,
        mc=-1,
        e=None,
        ek=None,
        example=dedent(
            """\
        For SeriesGroupBy:

        >>> lst = ['a', 'a', 'b', 'b']
        >>> ser = pd.Series([1, 2, 3, 4], index=lst)
        >>> ser
        a    1
        a    2
        b    3
        b    4
        dtype: int64
        >>> ser.groupby(level=0).max()
        a    2
        b    4
        dtype: int64

        For DataFrameGroupBy:

        >>> data = [[1, 8, 2], [1, 2, 5], [2, 5, 8], [2, 6, 9]]
        >>> df = pd.DataFrame(data, columns=["a", "b", "c"],
        ...                   index=["tiger", "leopard", "cheetah", "lion"])
        >>> df
                  a  b  c
          tiger   1  8  2
        leopard   1  2  5
        cheetah   2  5  8
           lion   2  6  9
        >>> df.groupby("a").max()
            b  c
        a
        1   8  5
        2   6  9"""
        ),
    )
    def max(
        self,
        numeric_only: bool = False,
        min_count: int = -1,
        engine: Literal["cython", "numba"] | None = None,
        engine_kwargs: dict[str, bool] | None = None,
    ):
        if maybe_use_numba(engine):
            from pandas.core._numba.kernels import grouped_min_max

            return self._numba_agg_general(
                grouped_min_max,
                executor.identity_dtype_mapping,
                engine_kwargs,
                min_periods=min_count,
                is_max=True,
            )
        else:
            return self._agg_general(
                numeric_only=numeric_only,
                min_count=min_count,
                alias="max",
                npfunc=np.max,
            )
