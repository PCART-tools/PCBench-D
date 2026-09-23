    def __init__(
        self,
        *,
        parent: Resampler,
        groupby: GroupBy,
        key=None,
        selection: IndexLabel | None = None,
    ) -> None:
        # reached via ._gotitem and _get_resampler_for_grouping

        assert isinstance(groupby, GroupBy), type(groupby)

        # parent is always a Resampler, sometimes a _GroupByMixin
        assert isinstance(parent, Resampler), type(parent)

        # initialize our GroupByMixin object with
        # the resampler attributes
        for attr in self._attributes:
            setattr(self, attr, getattr(parent, attr))
        self._selection = selection

        self.binner = parent.binner
        self.key = key

        self._groupby = groupby
        self._timegrouper = copy.copy(parent._timegrouper)

        self.ax = parent.ax
        self.obj = parent.obj
