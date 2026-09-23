    @final
    @doc(_groupby_agg_method_template, fname="max", no=False, mc=-1)
    def max(self, numeric_only: bool = False, min_count: int = -1):
        return self._agg_general(
            numeric_only=numeric_only, min_count=min_count, alias="max", npfunc=np.max
        )
