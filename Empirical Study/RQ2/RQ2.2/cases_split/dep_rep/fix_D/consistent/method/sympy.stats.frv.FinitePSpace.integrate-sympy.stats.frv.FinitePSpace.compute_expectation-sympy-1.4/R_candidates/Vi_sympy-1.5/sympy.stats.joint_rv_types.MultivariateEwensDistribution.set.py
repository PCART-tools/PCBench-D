    @property
    def set(self):
        if not isinstance(self.n, Integer):
            i = Symbol('i', integer=True, positive=True)
            return Product(Intersection(S.Naturals0, Interval(0, self.n//i)),
                                    (i, 1, self.n))
        prod_set = Range(0, self.n + 1)
        for i in range(2, self.n + 1):
            prod_set *= Range(0, self.n//i + 1)
        return prod_set.flatten()
