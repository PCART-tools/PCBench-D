    def get_shared_x_axes(self):
        """Return an immutable view on the shared x-axes Grouper."""
        return cbook.GrouperView(self._shared_axes["x"])
