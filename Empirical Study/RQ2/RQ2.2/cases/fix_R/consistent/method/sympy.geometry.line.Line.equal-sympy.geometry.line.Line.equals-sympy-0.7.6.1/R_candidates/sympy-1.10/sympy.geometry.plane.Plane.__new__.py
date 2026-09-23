    def __new__(cls, p1, a=None, b=None, **kwargs):
        p1 = Point3D(p1, dim=3)
        if a and b:
            p2 = Point(a, dim=3)
            p3 = Point(b, dim=3)
            if Point3D.are_collinear(p1, p2, p3):
                raise ValueError('Enter three non-collinear points')
            a = p1.direction_ratio(p2)
            b = p1.direction_ratio(p3)
            normal_vector = tuple(Matrix(a).cross(Matrix(b)))
        else:
            a = kwargs.pop('normal_vector', a)
            evaluate = kwargs.get('evaluate', True)
            if is_sequence(a) and len(a) == 3:
                normal_vector = Point3D(a).args if evaluate else a
            else:
                raise ValueError(filldedent('''
                    Either provide 3 3D points or a point with a
                    normal vector expressed as a sequence of length 3'''))
            if all(coord.is_zero for coord in normal_vector):
                raise ValueError('Normal vector cannot be zero vector')
        return GeometryEntity.__new__(cls, p1, normal_vector, **kwargs)
