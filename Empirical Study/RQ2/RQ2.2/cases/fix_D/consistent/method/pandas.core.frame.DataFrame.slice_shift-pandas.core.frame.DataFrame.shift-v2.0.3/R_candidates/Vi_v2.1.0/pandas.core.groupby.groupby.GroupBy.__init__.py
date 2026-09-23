    @final
    def __init__(
        self,
        obj: NDFrameT,
        keys: _KeysArgType | None = None,
        axis: Axis = 0,
        level: IndexLabel | None = None,
        grouper: ops.BaseGrouper | None = None,
        exclusions: frozenset[Hashable] | None = None,
        selection: IndexLabel | None = None,
        as_index: bool = True,
        sort: bool = True,
        group_keys: bool = True,
        observed: bool | lib.NoDefault = lib.no_default,
        dropna: bool = True,
    ) -> None:
        self._selection = selection

        assert isinstance(obj, NDFrame), type(obj)

        self.level = level

        if not as_index:
            if axis != 0:
                raise ValueError("as_index=False only valid for axis=0")

        self.as_index = as_index
        self.keys = keys
        self.sort = sort
        self.group_keys = group_keys
        self.dropna = dropna

        if grouper is None:
            grouper, exclusions, obj = get_grouper(
                obj,
                keys,
                axis=axis,
                level=level,
                sort=sort,
                observed=False if observed is lib.no_default else observed,
                dropna=self.dropna,
            )

        if observed is lib.no_default:
            if any(ping._passed_categorical for ping in grouper.groupings):
                warnings.warn(
                    "The default of observed=False is deprecated and will be changed "
                    "to True in a future version of pandas. Pass observed=False to "
                    "retain current behavior or observed=True to adopt the future "
                    "default and silence this warning.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
            observed = False
        self.observed = observed

        self.obj = obj
        self.axis = obj._get_axis_number(axis)
        self.grouper = grouper
        self.exclusions = frozenset(exclusions) if exclusions else frozenset()
