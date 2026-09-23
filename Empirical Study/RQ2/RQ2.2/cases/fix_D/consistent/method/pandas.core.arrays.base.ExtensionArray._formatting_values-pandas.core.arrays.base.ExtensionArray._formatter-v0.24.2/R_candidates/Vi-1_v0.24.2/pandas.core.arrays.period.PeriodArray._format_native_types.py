    def _format_native_types(self, na_rep=u'NaT', date_format=None, **kwargs):
        """
        actually format my specific types
        """
        values = self.astype(object)

        if date_format:
            formatter = lambda dt: dt.strftime(date_format)
        else:
            formatter = lambda dt: u'%s' % dt

        if self._hasnans:
            mask = self._isnan
            values[mask] = na_rep
            imask = ~mask
            values[imask] = np.array([formatter(dt) for dt
                                      in values[imask]])
        else:
            values = np.array([formatter(dt) for dt in values])
        return values
