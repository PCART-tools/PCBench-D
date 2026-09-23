    @classmethod
    def construct_from_string(cls, string):
        """
        attempt to construct this type from a string, raise a TypeError
        if its not possible
        """
        if isinstance(string, compat.string_types):
            try:
                return cls(string)
            except ValueError:
                pass
        raise TypeError("could not construct IntervalDtype")
