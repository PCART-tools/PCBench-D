    @classmethod
    def unit_regular_asterisk(cls, numVertices):
        """
        Return a :class:`Path` for a unit regular
        asterisk with the given numVertices and radius of 1.0,
        centered at (0, 0).
        """
        return cls.unit_regular_star(numVertices, 0.0)
