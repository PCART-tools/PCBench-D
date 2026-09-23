    @cbook.deprecated("3.2")
    def is_unit(self):
        """Return whether this is the unit box (from (0, 0) to (1, 1))."""
        return self.get_points().tolist() == [[0., 0.], [1., 1.]]
