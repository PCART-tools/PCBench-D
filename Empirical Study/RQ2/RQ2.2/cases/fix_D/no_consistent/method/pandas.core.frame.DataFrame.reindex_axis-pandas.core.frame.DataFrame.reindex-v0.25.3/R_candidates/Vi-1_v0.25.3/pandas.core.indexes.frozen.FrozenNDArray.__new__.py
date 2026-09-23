    def __new__(cls, data, dtype=None, copy=False):
        warnings.warn(
            "\nFrozenNDArray is deprecated and will be removed in a "
            "future version.\nPlease use `numpy.ndarray` instead.\n",
            FutureWarning,
            stacklevel=2,
        )

        if copy is None:
            copy = not isinstance(data, FrozenNDArray)
        res = np.array(data, dtype=dtype, copy=copy).view(cls)
        return res
