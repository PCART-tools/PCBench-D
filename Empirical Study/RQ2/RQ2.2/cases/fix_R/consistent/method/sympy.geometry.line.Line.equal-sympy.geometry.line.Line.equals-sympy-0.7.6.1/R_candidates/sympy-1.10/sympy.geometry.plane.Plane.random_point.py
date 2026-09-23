    def random_point(self, seed=None):
        """ Returns a random point on the Plane.

        Returns
        =======

        Point3D

        Examples
        ========

        >>> from sympy import Plane
        >>> p = Plane((1, 0, 0), normal_vector=(0, 1, 0))
        >>> r = p.random_point(seed=42)  # seed value is optional
        >>> r.n(3)
        Point3D(2.29, 0, -1.35)

        The random point can be moved to lie on the circle of radius
        1 centered on p1:

        >>> c = p.p1 + (r - p.p1).unit
        >>> c.distance(p.p1).equals(1)
        True
        """
        if seed is not None:
            rng = random.Random(seed)
        else:
            rng = random
        u, v = Dummy('u'), Dummy('v')
        params = {
            u: 2*Rational(rng.gauss(0, 1)) - 1,
            v: 2*Rational(rng.gauss(0, 1)) - 1}
        return self.arbitrary_point(u, v).subs(params)
