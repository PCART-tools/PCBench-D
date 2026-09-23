    @final
    @doc(_groupby_agg_method_template, fname="prod", no=True, mc=0)
    def prod(
        self, numeric_only: bool | lib.NoDefault = lib.no_default, min_count: int = 0
    ):
        numeric_only = self._resolve_numeric_only(numeric_only)

        return self._agg_general(
            numeric_only=numeric_only, min_count=min_count, alias="prod", npfunc=np.prod
        )
