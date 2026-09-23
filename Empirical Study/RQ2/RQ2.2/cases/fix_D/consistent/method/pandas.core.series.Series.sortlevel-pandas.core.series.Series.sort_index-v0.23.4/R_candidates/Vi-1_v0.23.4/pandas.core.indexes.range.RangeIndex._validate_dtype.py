    @staticmethod
    def _validate_dtype(dtype):
        """ require dtype to be None or int64 """
        if not (dtype is None or is_int64_dtype(dtype)):
            raise TypeError('Invalid to pass a non-int64 dtype to RangeIndex')
