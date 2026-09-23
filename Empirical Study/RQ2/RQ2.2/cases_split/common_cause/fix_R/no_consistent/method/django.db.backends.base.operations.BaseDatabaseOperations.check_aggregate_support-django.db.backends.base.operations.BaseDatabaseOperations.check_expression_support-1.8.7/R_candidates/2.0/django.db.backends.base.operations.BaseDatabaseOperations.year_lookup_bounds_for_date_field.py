    def year_lookup_bounds_for_date_field(self, value):
        """
        Return a two-elements list with the lower and upper bound to be used
        with a BETWEEN operator to query a DateField value using a year
        lookup.

        `value` is an int, containing the looked-up year.
        """
        first = datetime.date(value, 1, 1)
        second = datetime.date(value, 12, 31)
        first = self.adapt_datefield_value(first)
        second = self.adapt_datefield_value(second)
        return [first, second]
