    def _validate_fill_value(self, value):
        """
        Convert value to be insertable to ndarray.
        """
        if is_bool(value) or is_bool_dtype(value):
            # force conversion to object
            # so we don't lose the bools
            raise TypeError
        elif isinstance(value, str) or lib.is_complex(value):
            raise TypeError
        elif is_scalar(value) and isna(value):
            if is_valid_nat_for_dtype(value, self.dtype):
                value = self._na_value
            else:
                # NaT, np.datetime64("NaT"), np.timedelta64("NaT")
                raise TypeError

        return value
