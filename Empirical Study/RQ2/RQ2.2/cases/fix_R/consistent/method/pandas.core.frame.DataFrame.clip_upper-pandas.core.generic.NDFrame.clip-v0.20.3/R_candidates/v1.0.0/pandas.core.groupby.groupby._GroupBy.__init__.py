    def __init__(
        self,
        obj: NDFrame,
        keys: Optional[_KeysArgType] = None,
        axis: int = 0,
        level=None,
        grouper: "Optional[ops.BaseGrouper]" = None,
        exclusions=None,
        selection=None,
        as_index: bool = True,
        sort: bool = True,
        group_keys: bool = True,
        squeeze: bool = False,
        observed: bool = False,
        mutated: bool = False,
    ):

        self._selection = selection

        assert isinstance(obj, NDFrame), type(obj)
        obj._consolidate_inplace()

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
            )

        self.obj = obj
        self.axis = obj._get_axis_number(axis)
        self.grouper = grouper
        self.exclusions = set(exclusions) if exclusions else set()
