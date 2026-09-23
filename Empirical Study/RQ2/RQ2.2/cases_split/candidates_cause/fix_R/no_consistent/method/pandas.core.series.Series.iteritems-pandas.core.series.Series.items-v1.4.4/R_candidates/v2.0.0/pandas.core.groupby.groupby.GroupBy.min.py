    @final
    @doc(_groupby_agg_method_template, fname="min", no=False, mc=-1)
    def min(
        self,
        numeric_only: bool = False,
        min_count: int = -1,
        engine: str | None = None,
        engine_kwargs: dict[str, bool] | None = None,
    ):
        if maybe_use_numba(engine):
            from pandas.core._numba.kernels import sliding_min_max

            return self._numba_agg_general(sliding_min_max, engine_kwargs, False)
        else:
            return self._agg_general(
                numeric_only=numeric_only,
                min_count=min_count,
                alias="min",
                npfunc=np.min,
            )
