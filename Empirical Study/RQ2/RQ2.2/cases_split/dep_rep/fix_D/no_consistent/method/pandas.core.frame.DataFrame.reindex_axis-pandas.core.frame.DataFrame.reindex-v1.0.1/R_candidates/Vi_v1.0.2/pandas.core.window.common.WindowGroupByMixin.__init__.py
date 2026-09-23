    def __init__(self, obj, *args, **kwargs):
        kwargs.pop("parent", None)
        groupby = kwargs.pop("groupby", None)
        if groupby is None:
            groupby, obj = obj, obj.obj
        self._groupby = groupby
        self._groupby.mutated = True
        self._groupby.grouper.mutated = True
        super().__init__(obj, *args, **kwargs)
