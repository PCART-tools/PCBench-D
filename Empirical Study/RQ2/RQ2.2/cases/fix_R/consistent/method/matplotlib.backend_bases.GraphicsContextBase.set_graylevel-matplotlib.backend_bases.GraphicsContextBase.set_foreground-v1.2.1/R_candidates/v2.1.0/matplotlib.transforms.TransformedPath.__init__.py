    def __init__(self, path, transform):
        """
        Create a new :class:`TransformedPath` from the given
        :class:`~matplotlib.path.Path` and :class:`Transform`.
        """
        if not isinstance(transform, Transform):
            msg = ("'transform' must be an instance of"
                   " 'matplotlib.transform.Transform'")
            raise ValueError(msg)
        TransformNode.__init__(self)

        self._path = path
        self._transform = transform
        self.set_children(transform)
        self._transformed_path = None
        self._transformed_points = None
