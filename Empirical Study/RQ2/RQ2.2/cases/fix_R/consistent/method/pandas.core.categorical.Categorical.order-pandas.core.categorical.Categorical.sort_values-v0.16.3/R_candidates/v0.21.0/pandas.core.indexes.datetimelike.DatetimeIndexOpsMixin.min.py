    def min(self, axis=None, *args, **kwargs):
        """
        Return the minimum value of the Index or minimum along
        an axis.

        See also
        --------
        numpy.ndarray.min
        """
        nv.validate_min(args, kwargs)

        try:
            i8 = self.asi8

            # quick check
            if len(i8) and self.is_monotonic:
                if i8[0] != iNaT:
                    return self._box_func(i8[0])

            if self.hasnans:
                min_stamp = self[~self._isnan].asi8.min()
            else:
                min_stamp = i8.min()
            return self._box_func(min_stamp)
        except ValueError:
            return self._na_value
