    def rotate(self, angle=0, pt=None):
        """Rotate ``angle`` radians counterclockwise about Point ``pt``.

        Note: since the general ellipse is not supported, only rotations that
        are integer multiples of pi/2 are allowed.

        Examples
        ========

        >>> from sympy import Ellipse, pi
        >>> Ellipse((1, 0), 2, 1).rotate(pi/2)
        Ellipse(Point2D(0, 1), 1, 2)
        >>> Ellipse((1, 0), 2, 1).rotate(pi)
        Ellipse(Point2D(-1, 0), 2, 1)
        """
        if self.hradius == self.vradius:
            return self.func(self.center.rotate(angle, pt), self.hradius)
        if (angle/S.Pi).is_integer:
            return super().rotate(angle, pt)
        if (2*angle/S.Pi).is_integer:
            return self.func(self.center.rotate(angle, pt), self.vradius, self.hradius)
        # XXX see https://github.com/sympy/sympy/issues/2815 for general ellipes
        raise NotImplementedError('Only rotations of pi/2 are currently supported for Ellipse.')
