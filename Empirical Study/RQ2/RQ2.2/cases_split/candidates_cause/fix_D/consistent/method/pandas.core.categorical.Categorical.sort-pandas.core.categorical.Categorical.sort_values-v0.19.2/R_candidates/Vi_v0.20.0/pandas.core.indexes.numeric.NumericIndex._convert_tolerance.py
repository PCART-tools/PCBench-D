    def _convert_tolerance(self, tolerance):
        try:
            return float(tolerance)
        except ValueError:
            raise ValueError('tolerance argument for %s must be numeric: %r' %
                             (type(self).__name__, tolerance))
