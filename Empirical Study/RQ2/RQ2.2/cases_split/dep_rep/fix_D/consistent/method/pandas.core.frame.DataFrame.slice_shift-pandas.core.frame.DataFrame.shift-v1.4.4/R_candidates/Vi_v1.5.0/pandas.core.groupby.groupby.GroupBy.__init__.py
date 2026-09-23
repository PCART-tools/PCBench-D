    @final
    def __init__(
        self,
        obj: NDFrameT,
        keys: _KeysArgType | None = None,
        axis: int = 0,
        level: IndexLabel | None = None,
        grouper: ops.BaseGrouper | None = None,
        exclusions: frozenset[Hashable] | None = None,
        selection: IndexLabel | None = None,
        as_index: bool = True,
        sort: bool = True,
        group_keys: bool | lib.NoDefault = True,
        squeeze: bool = False,
        observed: bool = False,
        mutated: bool = False,
        dropna: bool = True,
    ) -> None:

        self._selection = selection

        assert isinstance(obj, NDFrame), type(obj)

        self.level = level

        if not as_index:
            if not isinstance(obj, DataFrame):
                raise TypeError("as_index=False only valid with DataFrame")
            if axis != 0:
                raise ValueError("as_index=False only valid for axis=0")

        self.as_index = as_index
        self.keys = keys
        self.sort = sort
        self.group_keys = group_keys
        self.squeeze = squeeze
        self.observed = observed
        self.mutated = mutated
        self.dropna = dropna

        if grouper is None:
            from pandas.core.groupby.grouper import get_grouper

            grouper, exclusions, obj = get_grouper(
                obj,
                keys,
                axis=axis,
                level=level,
                sort=sort,
                observed=observed,
                mutated=self.mutated,
                dropna=self.dropna,
            )

        self.obj = obj
        self.axis = obj._get_axis_number(axis)
        self.grouper = grouper
        self.exclusions = frozenset(exclusions) if exclusions else frozenset()
