    def _get_field(self, m):

        values = self.asi8
        hasnans = self.hasnans
        if hasnans:
            result = np.empty(len(self), dtype='float64')
            mask = self._isnan
            imask = ~mask
            result.flat[imask] = np.array(
                [getattr(Timedelta(val), m) for val in values[imask]])
            result[mask] = np.nan
        else:
            result = np.array([getattr(Timedelta(val), m)
                               for val in values], dtype='int64')
        return Index(result, name=self.name)
