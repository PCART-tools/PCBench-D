    def __new__(
        cls, center=None, hradius=None, vradius=None, eccentricity=None, **kwargs):
        hradius = sympify(hradius)
        vradius = sympify(vradius)

        eccentricity = sympify(eccentricity)

        if center is None:
            center = Point(0, 0)
        else:
            center = Point(center, dim=2)

        if len(center) != 2:
            raise ValueError('The center of "{}" must be a two dimensional point'.format(cls))

        if len(list(filter(lambda x: x is not None, (hradius, vradius, eccentricity)))) != 2:
            raise ValueError(filldedent('''
                Exactly two arguments of "hradius", "vradius", and
                "eccentricity" must not be None.'''))

        if eccentricity is not None:
            if eccentricity.is_negative:
                raise GeometryError("Eccentricity of ellipse/circle should lie between [0, 1)")
            elif hradius is None:
                hradius = vradius / sqrt(1 - eccentricity**2)
            elif vradius is None:
                vradius = hradius * sqrt(1 - eccentricity**2)

        if hradius == vradius:
            return Circle(center, hradius, **kwargs)

        if S.Zero in (hradius, vradius):
            return Segment(Point(center[0] - hradius, center[1] - vradius), Point(center[0] + hradius, center[1] + vradius))

        if hradius.is_real is False or vradius.is_real is False:
            raise GeometryError("Invalid value encountered when computing hradius / vradius.")

        return GeometryEntity.__new__(cls, center, hradius, vradius, **kwargs)
