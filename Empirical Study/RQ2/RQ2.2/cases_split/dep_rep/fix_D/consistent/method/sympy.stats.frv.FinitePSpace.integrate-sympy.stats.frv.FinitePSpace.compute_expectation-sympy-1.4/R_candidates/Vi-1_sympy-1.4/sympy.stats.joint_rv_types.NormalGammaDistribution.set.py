    @property
    def set(self):
        from sympy.sets.sets import Interval
        return S.Reals*Interval(0, S.Infinity)
