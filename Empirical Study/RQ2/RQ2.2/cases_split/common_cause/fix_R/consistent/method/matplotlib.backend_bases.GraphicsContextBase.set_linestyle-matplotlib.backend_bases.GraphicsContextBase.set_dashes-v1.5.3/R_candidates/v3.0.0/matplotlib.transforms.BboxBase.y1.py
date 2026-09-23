    @property
    def y1(self):
        """
        :attr:`y1` is the second of the pair of *y* coordinates that
        define the bounding box. :attr:`y1` is not guaranteed to be greater
        than :attr:`y0`.  If you require that, use :attr:`ymax`.
        """
        return self.get_points()[1, 1]
