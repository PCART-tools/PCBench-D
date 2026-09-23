    @property
    def values(self):
        """Numpy representation of NDFrame

        Notes
        -----
        The dtype will be a lower-common-denominator dtype (implicit
        upcasting); that is to say if the dtypes (even of numeric types)
        are mixed, the one that accommodates all will be chosen. Use this
        with care if you are not dealing with the blocks.

        e.g. If the dtypes are float16 and float32, dtype will be upcast to
        float32.  If dtypes are int32 and uint8, dtype will be upcast to
        int32. By numpy.find_common_type convention, mixing int64 and uint64
        will result in a flot64 dtype.
        """
        return self.as_matrix()
