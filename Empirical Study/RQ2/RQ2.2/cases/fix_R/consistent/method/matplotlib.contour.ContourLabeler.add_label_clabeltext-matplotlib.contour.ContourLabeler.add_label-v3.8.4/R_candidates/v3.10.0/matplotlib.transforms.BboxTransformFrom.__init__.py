    def __init__(self, boxin, **kwargs):
        _api.check_isinstance(BboxBase, boxin=boxin)

        super().__init__(**kwargs)
        self._boxin = boxin
        self.set_children(boxin)
        self._mtx = None
        self._inverted = None
