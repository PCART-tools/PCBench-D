    def __init__(self, path, transform):
        """
        Parameters
        ----------
        path : `~.path.Path`
        transform : `Transform`
        """
        _api.check_isinstance(Transform, transform=transform)
        super().__init__()
        self._path = path
        self._transform = transform
        self.set_children(transform)
        self._transformed_path = None
        self._transformed_points = None
