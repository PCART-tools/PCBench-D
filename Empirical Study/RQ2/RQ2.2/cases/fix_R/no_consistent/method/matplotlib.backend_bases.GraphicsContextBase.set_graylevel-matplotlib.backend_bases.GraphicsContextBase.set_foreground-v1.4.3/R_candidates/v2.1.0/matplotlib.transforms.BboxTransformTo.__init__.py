    def __init__(self, boxout, **kwargs):
        """
        Create a new :class:`BboxTransformTo` that linearly transforms
        points from the unit bounding box to *boxout*.
        """
        if not boxout.is_bbox:
            raise ValueError("'boxout' must be bbox")

        Affine2DBase.__init__(self, **kwargs)
        self._boxout = boxout
        self.set_children(boxout)
        self._mtx = None
        self._inverted = None
