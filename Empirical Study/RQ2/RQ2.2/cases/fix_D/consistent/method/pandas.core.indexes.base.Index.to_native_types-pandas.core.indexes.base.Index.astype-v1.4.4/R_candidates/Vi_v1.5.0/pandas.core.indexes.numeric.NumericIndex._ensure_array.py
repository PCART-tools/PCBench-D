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

            orig = data
            data = np.asarray(data, dtype=dtype)
            if dtype is None and data.dtype.kind == "f":
                if cls is UInt64Index and (data >= 0).all():
                    # https://github.com/numpy/numpy/issues/19146
                    data = np.asarray(orig, dtype=np.uint64)

        if issubclass(data.dtype.type, str):
            cls._string_data_error(data)

        dtype = cls._ensure_dtype(dtype)

        if copy or not is_dtype_equal(data.dtype, dtype):
            # TODO: the try/except below is because it's difficult to predict the error
            # and/or error message from different combinations of data and dtype.
            # Efforts to avoid this try/except welcome.
            # See https://github.com/pandas-dev/pandas/pull/41153#discussion_r676206222
            try:
                subarr = np.array(data, dtype=dtype, copy=copy)
                cls._validate_dtype(subarr.dtype)
            except (TypeError, ValueError):
                raise ValueError(f"data is not compatible with {cls.__name__}")
            cls._assert_safe_casting(data, subarr)
        else:
            subarr = data

        if subarr.ndim > 1:
            # GH#13601, GH#20285, GH#27125
            raise ValueError("Index data must be 1-dimensional")

        subarr = np.asarray(subarr)
        return subarr
