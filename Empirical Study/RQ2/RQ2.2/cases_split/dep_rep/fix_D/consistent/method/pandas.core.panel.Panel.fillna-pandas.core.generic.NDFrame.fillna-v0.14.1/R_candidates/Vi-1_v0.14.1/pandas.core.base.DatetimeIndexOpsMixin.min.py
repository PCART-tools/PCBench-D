    def min(self, axis=None):
        """
        Overridden ndarray.min to return an object
        """
        try:
            i8 = self.asi8

            # quick check
            if len(i8) and self.is_monotonic:
                if i8[0] != tslib.iNaT:
                    return self._box_func(i8[0])

            if self.hasnans:
                mask = i8 == tslib.iNaT
                min_stamp = self[~mask].asi8.min()
            else:
                min_stamp = i8.min()
            return self._box_func(min_stamp)
        except ValueError:
            return self._na_value
