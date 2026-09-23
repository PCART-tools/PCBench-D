    def _convert_tolerance(self, tolerance):
        try:
            return Timedelta(tolerance).to_timedelta64()
        except ValueError:
            raise ValueError('tolerance argument for %s must be convertible '
                             'to Timedelta: %r'
                             % (type(self).__name__, tolerance))
