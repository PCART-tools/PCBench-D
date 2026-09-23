    def _try_cast(self, result, obj, numeric_only: bool = False):
        """
        Try to cast the result to our obj original type,
        we may have roundtripped through object in the mean-time.

        If numeric_only is True, then only try to cast numerics
        and not datetimelikes.

        """
        if obj.ndim > 1:
            dtype = obj._values.dtype
        else:
            dtype = obj.dtype

        if not is_scalar(result):
            if is_extension_array_dtype(dtype) and dtype.kind != "M":
                # The function can return something of any type, so check
                #  if the type is compatible with the calling EA.
                # datetime64tz is handled correctly in agg_series,
                #  so is excluded here.

                if len(result) and isinstance(result[0], dtype.type):
                    cls = dtype.construct_array_type()
                    result = try_cast_to_ea(cls, result, dtype=dtype)

            elif numeric_only and is_numeric_dtype(dtype) or not numeric_only:
                result = maybe_downcast_to_dtype(result, dtype)

        return result
