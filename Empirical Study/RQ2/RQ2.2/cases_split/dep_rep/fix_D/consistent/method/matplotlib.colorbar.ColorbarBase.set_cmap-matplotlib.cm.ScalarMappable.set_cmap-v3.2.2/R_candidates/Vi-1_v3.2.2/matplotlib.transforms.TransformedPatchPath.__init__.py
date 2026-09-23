    def __init__(self, patch):
        """
        Parameters
        ----------
        patch : `~.patches.Patch`
        """
        TransformNode.__init__(self)

        transform = patch.get_transform()
        self._patch = patch
        self._transform = transform
        self.set_children(transform)
        self._path = patch.get_path()
        self._transformed_path = None
        self._transformed_points = None
