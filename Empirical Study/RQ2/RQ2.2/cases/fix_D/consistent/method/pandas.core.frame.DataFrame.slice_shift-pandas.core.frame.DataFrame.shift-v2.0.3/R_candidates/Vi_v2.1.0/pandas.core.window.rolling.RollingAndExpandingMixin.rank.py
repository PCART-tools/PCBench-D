    def rank(
        self,
        method: WindowingRankType = "average",
        ascending: bool = True,
        pct: bool = False,
        numeric_only: bool = False,
    ):
        window_func = partial(
            window_aggregations.roll_rank,
            method=method,
            ascending=ascending,
            percentile=pct,
        )

        return self._apply(window_func, name="rank", numeric_only=numeric_only)
