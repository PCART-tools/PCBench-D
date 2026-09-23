    @final
    @doc(_groupby_agg_method_template, fname="sum", no=True, mc=0)
    def sum(
        self,
        numeric_only: bool | lib.NoDefault = lib.no_default,
        min_count: int = 0,
        engine: str | None = None,
        engine_kwargs: dict[str, bool] | None = None,
    ):
        if maybe_use_numba(engine):
            from pandas.core._numba.kernels import sliding_sum

            return self._numba_agg_general(
                sliding_sum,
                engine_kwargs,
                "groupby_sum",
            )
        else:
            numeric_only = self._resolve_numeric_only(numeric_only)

            # If we are grouping on categoricals we want unobserved categories to
            # return zero, rather than the default of NaN which the reindexing in
            # _agg_general() returns. GH #31422
            with com.temp_setattr(self, "observed", True):
                result = self._agg_general(
                    numeric_only=numeric_only,
                    min_count=min_count,
                    alias="add",
                    npfunc=np.sum,
                )

            return self._reindex_output(result, fill_value=0)
