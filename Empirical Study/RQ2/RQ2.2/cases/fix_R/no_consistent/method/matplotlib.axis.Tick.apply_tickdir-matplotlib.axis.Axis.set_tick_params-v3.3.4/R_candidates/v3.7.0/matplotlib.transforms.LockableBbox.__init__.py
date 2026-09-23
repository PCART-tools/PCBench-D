    def __init__(self, bbox, x0=None, y0=None, x1=None, y1=None, **kwargs):
        """
        Parameters
        ----------
        bbox : `Bbox`
            The child bounding box to wrap.

        x0 : float or None
            The locked value for x0, or None to leave unlocked.

        y0 : float or None
            The locked value for y0, or None to leave unlocked.

        x1 : float or None
            The locked value for x1, or None to leave unlocked.

        y1 : float or None
            The locked value for y1, or None to leave unlocked.

        """
        if not bbox.is_bbox:
            raise ValueError("'bbox' is not a bbox")

        super().__init__(**kwargs)
        self._bbox = bbox
        self.set_children(bbox)
        self._points = None
        fp = [x0, y0, x1, y1]
        mask = [val is None for val in fp]
        self._locked_points = np.ma.array(fp, float, mask=mask).reshape((2, 2))
