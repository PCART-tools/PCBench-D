    @classmethod
    def unit_rectangle(cls):
        """
        Return a `Path` instance of the unit rectangle from (0, 0) to (1, 1).
        """
        if cls._unit_rectangle is None:
            cls._unit_rectangle = \
                cls([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0],
                     [0.0, 0.0]],
                    [cls.MOVETO, cls.LINETO, cls.LINETO, cls.LINETO,
                     cls.CLOSEPOLY],
                    readonly=True)
        return cls._unit_rectangle
