    @property
    def intervalx(self):
        """
        :attr:`intervalx` is the pair of *x* coordinates that define
        the bounding box. It is not guaranteed to be sorted from left to right.
        """
        return self.get_points()[:, 0]
