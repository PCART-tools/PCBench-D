    @property
    def y0(self):
        """
        :attr:`y0` is the first of the pair of *y* coordinates that
        define the bounding box. :attr:`y0` is not guaranteed to be less than
        :attr:`y1`.  If you require that, use :attr:`ymin`.
        """
        return self.get_points()[0, 1]
