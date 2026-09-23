    def pdf(self, *x):
        dist = self.args[0]
        z = Dummy('z')
        if isinstance(dist, ContinuousDistribution):
            rv = SingleContinuousPSpace(z, dist).value
        elif isinstance(dist, DiscreteDistribution):
            rv = SingleDiscretePSpace(z, dist).value
        return MarginalDistribution(self, (rv,)).pdf(*x)
