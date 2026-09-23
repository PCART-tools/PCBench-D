    @property
    def x1(self):
        """
        (property) :attr:`x1` is the second of the pair of *x* coordinates that
        define the bounding box. :attr:`x1` is not guaranteed to be greater
        than :attr:`x0`.  If you require that, use :attr:`xmax`.
        """
        return self.get_points()[1, 0]
