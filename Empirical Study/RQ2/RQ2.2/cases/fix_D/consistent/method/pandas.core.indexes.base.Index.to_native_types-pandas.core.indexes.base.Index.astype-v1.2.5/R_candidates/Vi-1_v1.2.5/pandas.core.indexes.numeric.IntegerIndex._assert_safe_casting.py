    @classmethod
    def _assert_safe_casting(cls, data, subarr):
        """
        Ensure incoming data can be represented with matching signed-ness.
        """
        if data.dtype.kind != cls._default_dtype.kind:
            if not np.array_equal(data, subarr):
                raise TypeError("Unsafe NumPy casting, you must explicitly cast")
