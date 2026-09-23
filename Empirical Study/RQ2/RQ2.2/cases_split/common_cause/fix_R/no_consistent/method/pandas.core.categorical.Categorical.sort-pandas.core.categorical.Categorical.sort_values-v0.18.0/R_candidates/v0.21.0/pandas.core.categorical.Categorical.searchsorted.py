    @Substitution(klass='Categorical')
    @Appender(_shared_docs['searchsorted'])
    @deprecate_kwarg(old_arg_name='v', new_arg_name='value')
    def searchsorted(self, value, side='left', sorter=None):
        if not self.ordered:
            raise ValueError("Categorical not ordered\nyou can use "
                             ".as_ordered() to change the Categorical to an "
                             "ordered one")

        from pandas.core.series import Series

        values_as_codes = _get_codes_for_values(Series(value).values,
                                                self.categories)

        if -1 in values_as_codes:
            raise ValueError("Value(s) to be inserted must be in categories.")

        return self.codes.searchsorted(values_as_codes, side=side,
                                       sorter=sorter)
