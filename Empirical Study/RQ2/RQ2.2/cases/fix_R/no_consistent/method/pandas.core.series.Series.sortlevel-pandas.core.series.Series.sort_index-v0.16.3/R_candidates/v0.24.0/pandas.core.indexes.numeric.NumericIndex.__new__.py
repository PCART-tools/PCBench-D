    def __new__(cls, data=None, dtype=None, copy=False, name=None,
                fastpath=None):

        if fastpath is not None:
            warnings.warn("The 'fastpath' keyword is deprecated, and will be "
                          "removed in a future version.",
                          FutureWarning, stacklevel=2)
            if fastpath:
                return cls._simple_new(data, name=name)

        # is_scalar, generators handled in coerce_to_ndarray
        data = cls._coerce_to_ndarray(data)

        if issubclass(data.dtype.type, compat.string_types):
            cls._string_data_error(data)

        if copy or not is_dtype_equal(data.dtype, cls._default_dtype):
            subarr = np.array(data, dtype=cls._default_dtype, copy=copy)
            cls._assert_safe_casting(data, subarr)
        else:
            subarr = data

        if name is None and hasattr(data, 'name'):
            name = data.name
        return cls._simple_new(subarr, name=name)
