    def __contains__(self, o):
        x, y, z = map(Dummy, 'xyz')
        k = self.equation(x, y, z)
        if isinstance(o, (LinearEntity, LinearEntity3D)):
            t = Dummy()
            d = Point3D(o.arbitrary_point(t))
            e = k.subs([(x, d.x), (y, d.y), (z, d.z)])
            return e.equals(0)
        try:
            o = Point(o, dim=3, strict=True)
            d = k.xreplace(dict(zip((x, y, z), o.args)))
            return d.equals(0)
        except TypeError:
            return False
