    @property
    def size(self):
        """
        (property) The width and height of the bounding box.  May be negative,
        in the same way as :attr:`width` and :attr:`height`.
        """
        points = self.get_points()
        return points[1] - points[0]
