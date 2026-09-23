    def where(self, condition):
        rvs = frozenset(random_symbols(condition))
        if not (len(rvs) == 1 and rvs.issubset(self.values)):
            raise NotImplementedError(
                "Multiple continuous random variables not supported")
        rv = tuple(rvs)[0]
        interval = reduce_rational_inequalities_wrap(condition, rv)
        interval = interval.intersect(self.domain.set)
        return SingleContinuousDomain(rv.symbol, interval)
