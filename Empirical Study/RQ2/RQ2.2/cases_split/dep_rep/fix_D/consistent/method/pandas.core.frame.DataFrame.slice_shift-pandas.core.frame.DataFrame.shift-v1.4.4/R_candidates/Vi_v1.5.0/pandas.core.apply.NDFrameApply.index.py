    @property
    def index(self) -> Index:
        # error: Argument 1 to "__get__" of "AxisProperty" has incompatible type
        # "Union[Series, DataFrame, GroupBy[Any], SeriesGroupBy,
        # DataFrameGroupBy, BaseWindow, Resampler]"; expected "Union[DataFrame,
        # Series]"
        return self.obj.index  # type:ignore[arg-type]
