    def argmin(self, axis=None, *args, **kwargs):
        """
        Returns the indices of the minimum values along an axis.
        See `numpy.ndarray.argmin` for more information on the
        `axis` parameter.

        See also
        --------
        numpy.ndarray.argmin
        """
        nv.validate_argmin(args, kwargs)

        i8 = self.asi8
        if self.hasnans:
            mask = self._isnan
            if mask.all():
                return -1
            i8 = i8.copy()
            i8[mask] = np.iinfo('int64').max
        return i8.argmin()
