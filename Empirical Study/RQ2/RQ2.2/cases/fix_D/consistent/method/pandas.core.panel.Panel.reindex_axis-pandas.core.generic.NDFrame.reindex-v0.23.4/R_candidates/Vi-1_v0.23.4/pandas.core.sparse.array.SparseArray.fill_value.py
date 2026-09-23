    @fill_value.setter
    def fill_value(self, value):
        if not is_scalar(value):
            raise ValueError('fill_value must be a scalar')
        # if the specified value triggers type promotion, raise ValueError
        new_dtype, fill_value = maybe_promote(self.dtype, value)
        if is_dtype_equal(self.dtype, new_dtype):
            self._fill_value = fill_value
        else:
            msg = 'unable to set fill_value {fill} to {dtype} dtype'
            raise ValueError(msg.format(fill=value, dtype=self.dtype))
