    @property
    def intervaly(self):
        """
        :attr:`intervaly` is the pair of *y* coordinates that define
        the bounding box.  It is not guaranteed to be sorted from bottom to
        top.
        """
        return self.get_points()[:, 1]
