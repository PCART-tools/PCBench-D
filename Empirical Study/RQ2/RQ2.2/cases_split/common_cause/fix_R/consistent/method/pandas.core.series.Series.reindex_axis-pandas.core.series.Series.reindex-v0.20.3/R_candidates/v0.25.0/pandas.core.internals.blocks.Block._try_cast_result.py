    def _try_cast_result(self, result, dtype=None):
        """ try to cast the result to our original type, we may have
        roundtripped thru object in the mean-time
        """
        if dtype is None:
            dtype = self.dtype

        if self.is_integer or self.is_bool or self.is_datetime:
            pass
        elif self.is_float and result.dtype == self.dtype:
            # protect against a bool/object showing up here
            if isinstance(dtype, str) and dtype == "infer":
                return result

            # This is only reached via Block.setitem, where dtype is always
            #  either "infer", self.dtype, or values.dtype.
            assert dtype == self.dtype, (dtype, self.dtype)
            return result

        # may need to change the dtype here
        return maybe_downcast_to_dtype(result, dtype)
