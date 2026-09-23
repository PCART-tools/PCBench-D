    def __init__(self, path, transform):
        """
        Parameters
        ----------
        path : `~.path.Path`
        transform : `Transform`
        """
        cbook._check_isinstance(Transform, transform=transform)
        TransformNode.__init__(self)
        self._path = path
        self._transform = transform
        self.set_children(transform)
        self._transformed_path = None
        self._transformed_points = None
