    def __init__(self, boxin, boxout, **kwargs):
        """
        Create a new :class:`BboxTransform` that linearly transforms
        points from *boxin* to *boxout*.
        """
        if not boxin.is_bbox or not boxout.is_bbox:
            raise ValueError("'boxin' and 'boxout' must be bbox")

        Affine2DBase.__init__(self, **kwargs)
        self._boxin = boxin
        self._boxout = boxout
        self.set_children(boxin, boxout)
        self._mtx = None
        self._inverted = None
