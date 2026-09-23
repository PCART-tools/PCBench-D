    @classmethod
    def is_dtype(cls, dtype):
        """
        Return a boolean if we if the passed type is an actual dtype that we
        can match (via string or type)
        """

        if isinstance(dtype, compat.string_types):
            if dtype.lower().startswith('interval'):
                try:
                    if cls.construct_from_string(dtype) is not None:
                        return True
                    else:
                        return False
                except ValueError:
                    return False
            else:
                return False
        return super(IntervalDtype, cls).is_dtype(dtype)
