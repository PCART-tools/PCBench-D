    def __init__(self, obj, groupby=None, axis=0, kind=None, **kwargs):
        self.groupby = groupby
        self.keys = None
        self.sort = True
        self.axis = axis
        self.kind = kind
        self.squeeze = False
        self.group_keys = True
        self.as_index = True
        self.exclusions = set()
        self.binner = None
        self.grouper = None

        if self.groupby is not None:
            self.groupby._set_grouper(self._convert_obj(obj), sort=True)
