    @doc(DataFrame.describe)
    def describe(self, **kwargs):
        with self._group_selection_context():
            result = self.apply(lambda x: x.describe(**kwargs))
            if self.axis == 1:
                return result.T
            return result.unstack()
