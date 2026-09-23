    def compute_density(self, expr, **kwargs):
        # https://en.wikipedia.org/wiki/Random_variable#Functions_of_random_variables
        if expr == self.value:
            return self.density
        y = Dummy('y')

        gs = solveset(expr - y, self.value, S.Reals)

        if isinstance(gs, Intersection) and S.Reals in gs.args:
            gs = list(gs.args[1])

        if not gs:
            raise ValueError("Can not solve %s for %s"%(expr, self.value))
        fx = self.compute_density(self.value)
        fy = sum(fx(g) * abs(g.diff(y)) for g in gs)
        return Lambda(y, fy)
