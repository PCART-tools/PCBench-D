    def __init__(
        self,
        obj: DataFrame | Series,
        groupby: TimeGrouper,
        axis: int = 0,
        kind=None,
        *,
        group_keys: bool | lib.NoDefault = lib.no_default,
        selection=None,
        **kwargs,
    ) -> None:
        self.groupby = groupby
        self.keys = None
        self.sort = True
        self.axis = axis
        self.kind = kind
        self.squeeze = False
        self.group_keys = group_keys
        self.as_index = True

        self.groupby._set_grouper(self._convert_obj(obj), sort=True)
        self.binner, self.grouper = self._get_binner()
        self._selection = selection
        if self.groupby.key is not None:
            self.exclusions = frozenset([self.groupby.key])
        else:
            self.exclusions = frozenset()
