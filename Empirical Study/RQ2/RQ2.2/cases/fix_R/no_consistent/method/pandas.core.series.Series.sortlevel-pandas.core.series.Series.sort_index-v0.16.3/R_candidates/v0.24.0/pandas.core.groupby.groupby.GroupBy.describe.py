    @Appender(DataFrame.describe.__doc__)
    def describe(self, **kwargs):
        with _group_selection_context(self):
            result = self.apply(lambda x: x.describe(**kwargs))
            if self.axis == 1:
                return result.T
            return result.unstack()
