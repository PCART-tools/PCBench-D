    @Substitution(klass='Categorical', value='v')
    @Appender(_shared_docs['searchsorted'])
    def searchsorted(self, v, side='left', sorter=None):
        if not self.ordered:
            raise ValueError("Categorical not ordered\nyou can use "
                             ".as_ordered() to change the Categorical to an "
                             "ordered one")

        from pandas.core.series import Series
        values_as_codes = self.categories.values.searchsorted(
            Series(v).values, side=side)

        return self.codes.searchsorted(values_as_codes, sorter=sorter)
