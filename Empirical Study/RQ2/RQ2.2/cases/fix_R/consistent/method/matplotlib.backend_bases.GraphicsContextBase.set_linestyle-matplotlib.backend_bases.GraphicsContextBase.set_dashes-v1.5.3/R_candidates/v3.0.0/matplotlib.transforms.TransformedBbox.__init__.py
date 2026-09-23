    def __init__(self, bbox, transform, **kwargs):
        """
        Parameters
        ----------
        bbox : :class:`Bbox`

        transform : :class:`Transform`
        """
        if not bbox.is_bbox:
            raise ValueError("'bbox' is not a bbox")
        if not isinstance(transform, Transform):
            raise ValueError("'transform' must be an instance of "
                             "'matplotlib.transform.Transform'")
        if transform.input_dims != 2 or transform.output_dims != 2:
            raise ValueError(
                "The input and output dimensions of 'transform' must be 2")

        BboxBase.__init__(self, **kwargs)
        self._bbox = bbox
        self._transform = transform
        self.set_children(bbox, transform)
        self._points = None
