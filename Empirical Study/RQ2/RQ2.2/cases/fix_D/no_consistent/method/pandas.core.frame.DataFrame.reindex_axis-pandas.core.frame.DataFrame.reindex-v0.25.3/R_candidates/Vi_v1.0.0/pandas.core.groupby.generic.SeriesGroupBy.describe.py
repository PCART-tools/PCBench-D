    @Appender(Series.describe.__doc__)
    def describe(self, **kwargs):
        result = self.apply(lambda x: x.describe(**kwargs))
        if self.axis == 1:
            return result.T
        return result.unstack()
