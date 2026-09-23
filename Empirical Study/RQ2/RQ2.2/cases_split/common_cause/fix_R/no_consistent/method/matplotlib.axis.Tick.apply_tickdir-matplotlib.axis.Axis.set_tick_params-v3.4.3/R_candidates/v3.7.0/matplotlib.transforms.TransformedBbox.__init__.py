    def __init__(self, bbox, transform, **kwargs):
        """
        Parameters
        ----------
        bbox : `Bbox`
        transform : `Transform`
        """
        if not bbox.is_bbox:
            raise ValueError("'bbox' is not a bbox")
        _api.check_isinstance(Transform, transform=transform)
        if transform.input_dims != 2 or transform.output_dims != 2:
            raise ValueError(
                "The input and output dimensions of 'transform' must be 2")

        super().__init__(**kwargs)
        self._bbox = bbox
        self._transform = transform
        self.set_children(bbox, transform)
        self._points = None
