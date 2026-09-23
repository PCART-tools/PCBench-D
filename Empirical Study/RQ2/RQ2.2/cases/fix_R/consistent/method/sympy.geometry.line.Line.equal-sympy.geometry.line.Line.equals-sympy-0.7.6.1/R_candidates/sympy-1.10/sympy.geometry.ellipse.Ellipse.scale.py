    def scale(self, x=1, y=1, pt=None):
        """Override GeometryEntity.scale since it is the major and minor
        axes which must be scaled and they are not GeometryEntities.

        Examples
        ========

        >>> from sympy import Ellipse
        >>> Ellipse((0, 0), 2, 1).scale(2, 4)
        Circle(Point2D(0, 0), 4)
        >>> Ellipse((0, 0), 2, 1).scale(2)
        Ellipse(Point2D(0, 0), 4, 1)
        """
        c = self.center
        if pt:
            pt = Point(pt, dim=2)
            return self.translate(*(-pt).args).scale(x, y).translate(*pt.args)
        h = self.hradius
        v = self.vradius
        return self.func(c.scale(x, y), hradius=h*x, vradius=v*y)
