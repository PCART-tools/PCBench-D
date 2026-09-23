    @Appender(DataFrame.describe.__doc__)
    @Substitution(name='groupby')
    @Appender(_doc_template)
    def describe(self, **kwargs):
        self._set_group_selection()
        result = self.apply(lambda x: x.describe(**kwargs))
        if self.axis == 1:
            return result.T
        return result.unstack()
