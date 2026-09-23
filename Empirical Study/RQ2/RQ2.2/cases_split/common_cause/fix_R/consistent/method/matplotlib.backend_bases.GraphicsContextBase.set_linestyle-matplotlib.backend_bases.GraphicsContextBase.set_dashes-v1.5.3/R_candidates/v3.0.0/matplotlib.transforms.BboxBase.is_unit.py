    def is_unit(self):
        """
        Returns True if the :class:`Bbox` is the unit bounding box
        from (0, 0) to (1, 1).
        """
        return list(self.get_points().flatten()) == [0., 0., 1., 1.]
