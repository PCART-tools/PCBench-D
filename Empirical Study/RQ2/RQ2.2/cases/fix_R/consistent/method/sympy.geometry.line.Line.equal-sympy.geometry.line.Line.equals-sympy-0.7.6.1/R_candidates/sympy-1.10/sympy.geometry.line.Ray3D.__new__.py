    def __new__(cls, p1, pt=None, direction_ratio=(), **kwargs):
        if isinstance(p1, LinearEntity3D):
            if pt is not None:
                raise ValueError('If p1 is a LinearEntity, pt must be None')
            p1, pt = p1.args
        else:
            p1 = Point(p1, dim=3)
        if pt is not None and len(direction_ratio) == 0:
            pt = Point(pt, dim=3)
        elif len(direction_ratio) == 3 and pt is None:
            pt = Point3D(p1.x + direction_ratio[0], p1.y + direction_ratio[1],
                         p1.z + direction_ratio[2])
        else:
            raise ValueError(filldedent('''
                A 2nd Point or keyword "direction_ratio" must be used.
            '''))

        return LinearEntity3D.__new__(cls, p1, pt, **kwargs)
