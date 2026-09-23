    @final
    @doc(_groupby_agg_method_template, fname="min", no=False, mc=-1)
    def min(self, numeric_only: bool = False, min_count: int = -1):
        return self._agg_general(
            numeric_only=numeric_only, min_count=min_count, alias="min", npfunc=np.min
        )
