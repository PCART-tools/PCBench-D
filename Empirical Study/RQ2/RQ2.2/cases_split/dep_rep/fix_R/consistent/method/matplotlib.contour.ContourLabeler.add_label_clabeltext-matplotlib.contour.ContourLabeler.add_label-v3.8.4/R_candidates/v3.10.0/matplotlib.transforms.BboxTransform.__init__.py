    def __init__(self, boxin, boxout, **kwargs):
        """
        Create a new `BboxTransform` that linearly transforms
        points from *boxin* to *boxout*.
        """
        _api.check_isinstance(BboxBase, boxin=boxin, boxout=boxout)

        super().__init__(**kwargs)
        self._boxin = boxin
        self._boxout = boxout
        self.set_children(boxin, boxout)
        self._mtx = None
        self._inverted = None
