    @classmethod
    def _assert_safe_casting(cls, data, subarr):
        """
        Ensure incoming data can be represented as ints.
        """
        if not issubclass(data.dtype.type, np.signedinteger):
            if not np.array_equal(data, subarr):
                raise TypeError("Unsafe NumPy casting, you must " "explicitly cast")
