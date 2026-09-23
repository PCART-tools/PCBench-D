    def astype(self, dtype=None, copy=True):
        dtype = np.dtype(dtype)
        sp_values = astype_nansafe(self.sp_values, dtype, copy=copy)
        try:
            if is_bool_dtype(dtype):
                # to avoid np.bool_ dtype
                fill_value = bool(self.fill_value)
            else:
                fill_value = dtype.type(self.fill_value)
        except ValueError:
            msg = 'unable to coerce current fill_value {0} to {1} dtype'
            raise ValueError(msg.format(self.fill_value, dtype))
        return self._simple_new(sp_values, self.sp_index,
                                fill_value=fill_value)
