    def __new__(cls, *args, **kwargs):
        evaluate = kwargs.get('evaluate', global_parameters.evaluate)
        if len(args) == 1 and isinstance(args[0], (Expr, Eq)):
            x = kwargs.get('x', 'x')
            y = kwargs.get('y', 'y')
            equation = args[0]
            if isinstance(equation, Eq):
                equation = equation.lhs - equation.rhs
            x = find(x, equation)
            y = find(y, equation)

            try:
                a, b, c, d, e = linear_coeffs(equation, x**2, y**2, x, y)
            except ValueError:
                raise GeometryError("The given equation is not that of a circle.")

            if S.Zero in (a, b) or a != b:
                raise GeometryError("The given equation is not that of a circle.")

            center_x = -c/a/2
            center_y = -d/b/2
            r2 = (center_x**2) + (center_y**2) - e

            return Circle((center_x, center_y), sqrt(r2), evaluate=evaluate)

        else:
            c, r = None, None
            if len(args) == 3:
                args = [Point(a, dim=2, evaluate=evaluate) for a in args]
                t = Triangle(*args)
                if not isinstance(t, Triangle):
                    return t
                c = t.circumcenter
                r = t.circumradius
            elif len(args) == 2:
                # Assume (center, radius) pair
                c = Point(args[0], dim=2, evaluate=evaluate)
                r = args[1]
                # this will prohibit imaginary radius
                try:
                    r = Point(r, 0, evaluate=evaluate).x
                except ValueError:
                    raise GeometryError("Circle with imaginary radius is not permitted")

            if not (c is None or r is None):
                if r == 0:
                    return c
                return GeometryEntity.__new__(cls, c, r, **kwargs)

            raise GeometryError("Circle.__new__ received unknown arguments")
