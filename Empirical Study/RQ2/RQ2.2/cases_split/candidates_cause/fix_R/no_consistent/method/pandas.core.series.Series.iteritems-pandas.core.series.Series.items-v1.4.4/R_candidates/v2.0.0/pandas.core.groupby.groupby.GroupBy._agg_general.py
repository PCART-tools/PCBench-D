    @final
    def _agg_general(
        self,
        numeric_only: bool = False,
        min_count: int = -1,
        *,
        alias: str,
        npfunc: Callable,
    ):
        result = self._cython_agg_general(
            how=alias,
            alt=npfunc,
            numeric_only=numeric_only,
            min_count=min_count,
        )
        return result.__finalize__(self.obj, method="groupby")
