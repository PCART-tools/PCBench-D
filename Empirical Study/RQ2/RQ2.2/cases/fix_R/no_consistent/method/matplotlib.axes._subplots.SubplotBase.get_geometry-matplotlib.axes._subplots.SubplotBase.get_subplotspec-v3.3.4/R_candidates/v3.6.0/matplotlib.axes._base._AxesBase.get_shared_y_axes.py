    def get_shared_y_axes(self):
        """Return an immutable view on the shared y-axes Grouper."""
        return cbook.GrouperView(self._shared_axes["y"])
