    def coerce_to_target_dtype(self, other):
        """
        coerce the current block to a dtype compat for other
        we will return a block, possibly object, and not raise

        we can also safely try to coerce to the same dtype
        and will receive the same block
        """

        # if we cannot then coerce to object
        dtype, _ = infer_dtype_from(other, pandas_dtype=True)

        if is_dtype_equal(self.dtype, dtype):
            return self

        if self.is_bool or is_object_dtype(dtype) or is_bool_dtype(dtype):
            # we don't upcast to bool
            return self.astype(object)

        elif (self.is_float or self.is_complex) and (
            is_integer_dtype(dtype) or is_float_dtype(dtype)
        ):
            # don't coerce float/complex to int
            return self

        elif (
            self.is_datetime
            or is_datetime64_dtype(dtype)
            or is_datetime64tz_dtype(dtype)
        ):

            # not a datetime
            if not (
                (is_datetime64_dtype(dtype) or is_datetime64tz_dtype(dtype))
                and self.is_datetime
            ):
                return self.astype(object)

            # don't upcast timezone with different timezone or no timezone
            mytz = getattr(self.dtype, "tz", None)
            othertz = getattr(dtype, "tz", None)

            if not tz_compare(mytz, othertz):
                return self.astype(object)

            raise AssertionError(
                f"possible recursion in coerce_to_target_dtype: {self} {other}"
            )

        elif self.is_timedelta or is_timedelta64_dtype(dtype):

            # not a timedelta
            if not (is_timedelta64_dtype(dtype) and self.is_timedelta):
                return self.astype(object)

            raise AssertionError(
                f"possible recursion in coerce_to_target_dtype: {self} {other}"
            )

        try:
            return self.astype(dtype)
        except (ValueError, TypeError, OverflowError):
            return self.astype(object)
