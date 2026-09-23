    @final
    @doc(_groupby_agg_method_template, fname="prod", no=False, mc=0)
    def prod(self, numeric_only: bool = False, min_count: int = 0):
        return self._agg_general(
            numeric_only=numeric_only, min_count=min_count, alias="prod", npfunc=np.prod
        )
