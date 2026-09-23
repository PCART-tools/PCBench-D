    @staticmethod
    def process_value(value):
        """
        Homogenize the input *value* for easy and efficient normalization.

        *value* can be a scalar or sequence.

        Returns *result*, *is_scalar*, where *result* is a
        masked array matching *value*.  Float dtypes are preserved;
        integer types with two bytes or smaller are converted to
        np.float32, and larger types are converted to np.float64.
        Preserving float32 when possible, and using in-place operations,
        can greatly improve speed for large arrays.

        Experimental; we may want to add an option to force the
        use of float32.
        """
        is_scalar = not np.iterable(value)
        if is_scalar:
            value = [value]
        dtype = np.min_scalar_type(value)
        if np.issubdtype(dtype, np.integer) or dtype.type is np.bool_:
            # bool_/int8/int16 -> float32; int32/int64 -> float64
            dtype = np.promote_types(dtype, np.float32)
        # ensure data passed in as an ndarray subclass are interpreted as
        # an ndarray. See issue #6622.
        mask = np.ma.getmask(value)
        data = np.asarray(np.ma.getdata(value))
        result = np.ma.array(data, mask=mask, dtype=dtype, copy=True)
        return result, is_scalar
