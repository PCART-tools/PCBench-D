    @classmethod
    def is_dtype(cls, dtype):
        """ Return a boolean if the passed type is an actual dtype that
        we can match (via string or type)
        """
        if hasattr(dtype, 'dtype'):
            dtype = dtype.dtype
        if isinstance(dtype, cls):
            return True
        elif isinstance(dtype, np.dtype):
            return False
        elif dtype is None:
            return False
        try:
            return cls.construct_from_string(dtype) is not None
        except:
            return False
