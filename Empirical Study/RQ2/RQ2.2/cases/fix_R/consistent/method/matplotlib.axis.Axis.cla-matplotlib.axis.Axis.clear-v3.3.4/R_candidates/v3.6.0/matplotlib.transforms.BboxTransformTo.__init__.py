    def __init__(self, boxout, **kwargs):
        """
        Create a new `BboxTransformTo` that linearly transforms
        points from the unit bounding box to *boxout*.
        """
        if not boxout.is_bbox:
            raise ValueError("'boxout' must be bbox")

        super().__init__(**kwargs)
        self._boxout = boxout
        self.set_children(boxout)
        self._mtx = None
        self._inverted = None
