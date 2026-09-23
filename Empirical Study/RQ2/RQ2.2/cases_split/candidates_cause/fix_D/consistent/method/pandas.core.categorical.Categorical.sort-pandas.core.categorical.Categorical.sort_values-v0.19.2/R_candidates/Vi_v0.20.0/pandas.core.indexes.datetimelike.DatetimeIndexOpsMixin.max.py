    def max(self, axis=None, *args, **kwargs):
        """
        Return the maximum value of the Index or maximum along
        an axis.

        See also
        --------
        numpy.ndarray.max
        """
        nv.validate_max(args, kwargs)

        try:
            i8 = self.asi8

            # quick check
            if len(i8) and self.is_monotonic:
                if i8[-1] != iNaT:
                    return self._box_func(i8[-1])

            if self.hasnans:
                max_stamp = self[~self._isnan].asi8.max()
            else:
                max_stamp = i8.max()
            return self._box_func(max_stamp)
        except ValueError:
            return self._na_value
