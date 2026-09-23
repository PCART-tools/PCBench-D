    def __init__(
        self,
        obj: DataFrame | Series,
        groupby: TimeGrouper,
        axis: int = 0,
        kind=None,
        *,
        selection=None,
        **kwargs,
    ):
        self.groupby = groupby
        self.keys = None
        self.sort = True
        self.axis = axis
        self.kind = kind
        self.squeeze = False
        self.group_keys = True
        self.as_index = True

        self.groupby._set_grouper(self._convert_obj(obj), sort=True)
        self.binner, self.grouper = self._get_binner()
        self._selection = selection
