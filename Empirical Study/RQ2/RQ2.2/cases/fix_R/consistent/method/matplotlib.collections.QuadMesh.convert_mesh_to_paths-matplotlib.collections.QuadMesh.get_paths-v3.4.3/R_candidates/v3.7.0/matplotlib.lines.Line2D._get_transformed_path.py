    def _get_transformed_path(self):
        """Return this line's `~matplotlib.transforms.TransformedPath`."""
        if self._transformed_path is None:
            self._transform_path()
        return self._transformed_path
