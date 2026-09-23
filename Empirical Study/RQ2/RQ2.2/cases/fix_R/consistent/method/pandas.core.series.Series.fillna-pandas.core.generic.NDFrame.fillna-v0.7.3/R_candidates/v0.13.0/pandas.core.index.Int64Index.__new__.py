    def __new__(cls, data, dtype=None, copy=False, name=None, fastpath=False):

        if fastpath:
            subarr = data.view(cls)
            subarr.name = name
            return subarr

        # isscalar, generators handled in coerce_to_ndarray
        data = cls._coerce_to_ndarray(data)

        if issubclass(data.dtype.type, compat.string_types):
            cls._string_data_error(data)

        elif issubclass(data.dtype.type, np.integer):
            # don't force the upcast as we may be dealing
            # with a platform int
            if dtype is None or not issubclass(np.dtype(dtype).type,
                                               np.integer):
                dtype = np.int64

            subarr = np.array(data, dtype=dtype, copy=copy)
        else:
            subarr = np.array(data, dtype=np.int64, copy=copy)
            if len(data) > 0:
                if (subarr != data).any():
                    raise TypeError('Unsafe NumPy casting to integer, you must'
                                    ' explicitly cast')

        subarr = subarr.view(cls)
        subarr.name = name
        return subarr
