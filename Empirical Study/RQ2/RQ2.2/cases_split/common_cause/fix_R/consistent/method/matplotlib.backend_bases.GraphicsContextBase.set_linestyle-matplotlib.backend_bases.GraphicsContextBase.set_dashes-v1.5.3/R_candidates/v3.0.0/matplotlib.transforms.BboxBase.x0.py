    @property
    def x0(self):
        """
        :attr:`x0` is the first of the pair of *x* coordinates that
        define the bounding box. :attr:`x0` is not guaranteed to be less than
        :attr:`x1`.  If you require that, use :attr:`xmin`.
        """
        return self.get_points()[0, 0]
