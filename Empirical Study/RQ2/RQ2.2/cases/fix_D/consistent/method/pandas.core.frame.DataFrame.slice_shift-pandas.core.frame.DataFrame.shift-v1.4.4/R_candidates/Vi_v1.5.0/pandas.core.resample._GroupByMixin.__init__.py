    def __init__(self, obj, parent=None, groupby=None, key=None, **kwargs) -> None:
        # reached via ._gotitem and _get_resampler_for_grouping

        if parent is None:
            parent = obj

        # initialize our GroupByMixin object with
        # the resampler attributes
        for attr in self._attributes:
            setattr(self, attr, kwargs.get(attr, getattr(parent, attr)))
        self._selection = kwargs.get("selection")

        self.binner = parent.binner
        self.key = key

        self._groupby = groupby
        self._groupby.mutated = True
        self._groupby.grouper.mutated = True
        self.groupby = copy.copy(parent.groupby)
