    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], (Expr, Eq)):
            missing = uniquely_named_symbol('?', args)
            if not kwargs:
                x = 'x'
                y = 'y'
            else:
                x = kwargs.pop('x', missing)
                y = kwargs.pop('y', missing)
            if kwargs:
                raise ValueError('expecting only x and y as keywords')

            equation = args[0]
            if isinstance(equation, Eq):
                equation = equation.lhs - equation.rhs

            def find_or_missing(x):
                try:
                    return find(x, equation)
                except ValueError:
                    return missing
            x = find_or_missing(x)
            y = find_or_missing(y)

            a, b, c = linear_coeffs(equation, x, y)

            if b:
                return Line((0, -c/b), slope=-a/b)
            if a:
                return Line((-c/a, 0), slope=oo)

            raise ValueError('not found in equation: %s' % (set('xy') - {x, y}))

        else:
            if len(args) > 0:
                p1 = args[0]
                if len(args) > 1:
                    p2 = args[1]
                else:
                    p2 = None

                if isinstance(p1, LinearEntity):
                    if p2:
                        raise ValueError('If p1 is a LinearEntity, p2 must be None.')
                    dim = len(p1.p1)
                else:
                    p1 = Point(p1)
                    dim = len(p1)
                    if p2 is not None or isinstance(p2, Point) and p2.ambient_dimension != dim:
                        p2 = Point(p2)

                if dim == 2:
                    return Line2D(p1, p2, **kwargs)
                elif dim == 3:
                    return Line3D(p1, p2, **kwargs)
                return LinearEntity.__new__(cls, p1, p2, **kwargs)
