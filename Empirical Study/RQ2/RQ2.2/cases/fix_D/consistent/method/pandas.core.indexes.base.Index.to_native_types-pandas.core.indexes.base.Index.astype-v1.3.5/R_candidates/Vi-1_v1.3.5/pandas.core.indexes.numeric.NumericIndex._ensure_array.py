    @classmethod
    def _ensure_array(cls, data, dtype, copy: bool):
        """
        Ensure we have a valid array to pass to _simple_new.
        """
        cls._validate_dtype(dtype)

        if not isinstance(data, (np.ndarray, Index)):
            # Coerce to ndarray if not already ndarray or Index
            if is_scalar(data):
                raise cls._scalar_data_error(data)

            # other iterable of some kind
            if not isinstance(data, (ABCSeries, list, tuple)):
                data = list(data)

            data = np.asarray(data, dtype=dtype)

        if issubclass(data.dtype.type, str):
            cls._string_data_error(data)

        dtype = cls._ensure_dtype(dtype)

        if copy or not is_dtype_equal(data.dtype, dtype):
            subarr = np.array(data, dtype=dtype, copy=copy)
            cls._assert_safe_casting(data, subarr)
        else:
            subarr = data

        if subarr.ndim > 1:
            # GH#13601, GH#20285, GH#27125
            raise ValueError("Index data must be 1-dimensional")

        subarr = np.asarray(subarr)
        return subarr
