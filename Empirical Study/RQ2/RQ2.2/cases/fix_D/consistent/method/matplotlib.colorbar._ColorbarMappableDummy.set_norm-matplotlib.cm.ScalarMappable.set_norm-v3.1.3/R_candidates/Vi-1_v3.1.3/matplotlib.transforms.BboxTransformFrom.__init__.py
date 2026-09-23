    def __init__(self, boxin, **kwargs):
        if not boxin.is_bbox:
            raise ValueError("'boxin' must be bbox")

        Affine2DBase.__init__(self, **kwargs)
        self._boxin = boxin
        self.set_children(boxin)
        self._mtx = None
        self._inverted = None
