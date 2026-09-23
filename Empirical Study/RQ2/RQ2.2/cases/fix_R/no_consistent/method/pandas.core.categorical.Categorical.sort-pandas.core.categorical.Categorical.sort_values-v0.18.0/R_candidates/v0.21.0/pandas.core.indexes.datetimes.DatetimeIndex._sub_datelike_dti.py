    def _sub_datelike_dti(self, other):
        """subtraction of two DatetimeIndexes"""
        if not len(self) == len(other):
            raise ValueError("cannot add indices of unequal length")

        self_i8 = self.asi8
        other_i8 = other.asi8
        new_values = self_i8 - other_i8
        if self.hasnans or other.hasnans:
            mask = (self._isnan) | (other._isnan)
            new_values[mask] = libts.iNaT
        return new_values.view('i8')
