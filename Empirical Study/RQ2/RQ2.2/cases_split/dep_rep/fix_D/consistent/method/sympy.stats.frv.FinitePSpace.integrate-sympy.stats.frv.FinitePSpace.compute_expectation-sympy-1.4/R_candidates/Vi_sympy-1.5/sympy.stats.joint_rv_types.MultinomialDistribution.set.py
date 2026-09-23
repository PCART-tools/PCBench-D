    @property
    def set(self):
        return Intersection(S.Naturals0, Interval(0, self.n))**len(self.p)
