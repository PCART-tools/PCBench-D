    def max(self, axis=None):
        """
        Overridden ndarray.max to return an object
        """
        try:
            i8 = self.asi8

            # quick check
            if len(i8) and self.is_monotonic:
                if i8[-1] != tslib.iNaT:
                    return self._box_func(i8[-1])

            if self.hasnans:
                mask = i8 == tslib.iNaT
                max_stamp = self[~mask].asi8.max()
            else:
                max_stamp = i8.max()
            return self._box_func(max_stamp)
        except ValueError:
            return self._na_value
