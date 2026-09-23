    def __new__(cls, data, dtype=None, copy=False, name=None, fastpath=False):

        if fastpath:
            subarr = data.view(cls)
            subarr.name = name
            return subarr

        data = cls._coerce_to_ndarray(data)

        if issubclass(data.dtype.type, compat.string_types):
            cls._string_data_error(data)

        if dtype is None:
            dtype = np.float64

        try:
            subarr = np.array(data, dtype=dtype, copy=copy)
        except:
            raise TypeError('Unsafe NumPy casting, you must '
                            'explicitly cast')

        # coerce to float64 for storage
        if subarr.dtype != np.float64:
            subarr = subarr.astype(np.float64)

        subarr = subarr.view(cls)
        subarr.name = name
        return subarr
