    @Substitution(klass='Categorical')
    @Appender(_shared_docs['searchsorted'])
    def searchsorted(self, value, side='left', sorter=None):
        if not self.ordered:
            raise ValueError("Categorical not ordered\nyou can use "
                             ".as_ordered() to change the Categorical to an "
                             "ordered one")

        from pandas.core.series import Series
        codes = _get_codes_for_values(Series(value).values, self.categories)
        if -1 in codes:
            raise KeyError("Value(s) to be inserted must be in categories.")

        codes = codes[0] if is_scalar(value) else codes

        return self.codes.searchsorted(codes, side=side, sorter=sorter)
