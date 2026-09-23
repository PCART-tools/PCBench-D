    def _sub_datetime_arraylike(self, other):
        """subtract DatetimeArray/Index or ndarray[datetime64]"""
        if len(self) != len(other):
            raise ValueError("cannot add indices of unequal length")

        if isinstance(other, np.ndarray):
            assert is_datetime64_dtype(other)
            other = type(self)(other)

        try:
            self._assert_tzawareness_compat(other)
        except TypeError as error:
            new_message = str(error).replace("compare", "subtract")
            raise type(error)(new_message) from error

        self_i8 = self.asi8
        other_i8 = other.asi8
        arr_mask = self._isnan | other._isnan
        new_values = checked_add_with_arr(self_i8, -other_i8, arr_mask=arr_mask)
        if self._hasna or other._hasna:
            np.putmask(new_values, arr_mask, iNaT)
        return new_values.view("timedelta64[ns]")
