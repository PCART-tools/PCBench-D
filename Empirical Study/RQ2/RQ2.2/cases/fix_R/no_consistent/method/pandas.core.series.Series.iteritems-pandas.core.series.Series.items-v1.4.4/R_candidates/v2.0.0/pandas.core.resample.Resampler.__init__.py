    def __init__(
        self,
        obj: NDFrame,
        timegrouper: TimeGrouper,
        axis: Axis = 0,
        kind=None,
        *,
        gpr_index: Index,
        group_keys: bool = False,
        selection=None,
    ) -> None:
        self._timegrouper = timegrouper
        self.keys = None
        self.sort = True
        self.axis = obj._get_axis_number(axis)
        self.kind = kind
        self.group_keys = group_keys
        self.as_index = True

        self.obj, self.ax, self._indexer = self._timegrouper._set_grouper(
            self._convert_obj(obj), sort=True, gpr_index=gpr_index
        )
        self.binner, self.grouper = self._get_binner()
        self._selection = selection
        if self._timegrouper.key is not None:
            self.exclusions = frozenset([self._timegrouper.key])
        else:
            self.exclusions = frozenset()
