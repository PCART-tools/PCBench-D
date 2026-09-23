    def __call__(
        self,
        n: PositionalIndexer | tuple,
        dropna: Literal["any", "all", None] = None,
    ) -> DataFrame | Series:
        return self.groupby_object._nth(n, dropna)
