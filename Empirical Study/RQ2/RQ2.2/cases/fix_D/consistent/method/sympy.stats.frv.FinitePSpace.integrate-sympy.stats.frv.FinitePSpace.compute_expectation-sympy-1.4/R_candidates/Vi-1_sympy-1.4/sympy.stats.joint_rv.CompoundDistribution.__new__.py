    def __new__(cls, dist):
        if not isinstance(dist, (ContinuousDistribution, DiscreteDistribution)):
            raise ValueError(filldedent('''CompoundDistribution can only be
             initialized from ContinuousDistribution or DiscreteDistribution
             '''))
        _args = dist.args
        if not any([isinstance(i, RandomSymbol) for i in _args]):
            return dist
        return Basic.__new__(cls, dist)
