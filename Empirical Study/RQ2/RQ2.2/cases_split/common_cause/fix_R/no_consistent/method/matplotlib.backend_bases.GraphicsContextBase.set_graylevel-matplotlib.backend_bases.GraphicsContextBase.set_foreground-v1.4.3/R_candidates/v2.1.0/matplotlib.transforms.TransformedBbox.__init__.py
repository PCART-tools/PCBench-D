    def __init__(self, bbox, transform, **kwargs):
        """
        *bbox*: a child :class:`Bbox`

        *transform*: a 2D :class:`Transform`
        """
        if not bbox.is_bbox:
            raise ValueError("'bbox' is not a bbox")
        if not isinstance(transform, Transform):
            msg = ("'transform' must be an instance of"
                   " 'matplotlib.transform.Transform'")
            raise ValueError(msg)
        if transform.input_dims != 2 or transform.output_dims != 2:
            msg = "The input and output dimensions of 'transform' must be 2"
            raise ValueError(msg)

        BboxBase.__init__(self, **kwargs)
        self._bbox = bbox
        self._transform = transform
        self.set_children(bbox, transform)
        self._points = None
