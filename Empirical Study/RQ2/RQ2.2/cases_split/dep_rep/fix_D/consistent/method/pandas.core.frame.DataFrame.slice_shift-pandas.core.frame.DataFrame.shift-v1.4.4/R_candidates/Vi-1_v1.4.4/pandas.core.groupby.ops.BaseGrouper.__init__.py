    def __init__(
        self,
        axis: Index,
        groupings: Sequence[grouper.Grouping],
        sort: bool = True,
        group_keys: bool = True,
        mutated: bool = False,
        indexer: npt.NDArray[np.intp] | None = None,
        dropna: bool = True,
    ):
        assert isinstance(axis, Index), axis

        self.axis = axis
        self._groupings: list[grouper.Grouping] = list(groupings)
        self._sort = sort
        self.group_keys = group_keys
        self.mutated = mutated
        self.indexer = indexer
        self.dropna = dropna
