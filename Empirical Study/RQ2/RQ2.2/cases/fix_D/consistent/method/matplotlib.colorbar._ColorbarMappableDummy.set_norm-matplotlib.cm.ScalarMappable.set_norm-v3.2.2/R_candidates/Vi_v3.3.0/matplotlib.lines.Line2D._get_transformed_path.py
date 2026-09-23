    def _get_transformed_path(self):
        """
        Return the :class:`~matplotlib.transforms.TransformedPath` instance
        of this line.
        """
        if self._transformed_path is None:
            self._transform_path()
        return self._transformed_path
