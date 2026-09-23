    def parameter_value(self, other, t):
        if not isinstance(other,GeometryEntity):
            other = Point(other, dim=self.ambient_dimension)
        if not isinstance(other,Point):
            raise ValueError("other must be a point")
        if other.free_symbols:
            raise NotImplementedError('non-numeric coordinates')
        unknown = False
        T = Dummy('t', real=True)
        p = self.arbitrary_point(T)
        for pt, cond in p.args:
            sol = solve(pt - other, T, dict=True)
            if not sol:
                continue
            value = sol[0][T]
            if simplify(cond.subs(T, value)) == True:
                return {t: value}
            unknown = True
        if unknown:
            raise ValueError("Given point may not be on %s" % func_name(self))
        raise ValueError("Given point is not on %s" % func_name(self))
