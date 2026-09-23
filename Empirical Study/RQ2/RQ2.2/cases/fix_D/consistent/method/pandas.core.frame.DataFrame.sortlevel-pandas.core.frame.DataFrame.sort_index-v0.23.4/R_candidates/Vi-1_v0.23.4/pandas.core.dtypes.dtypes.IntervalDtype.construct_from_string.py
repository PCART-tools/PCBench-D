    @classmethod
    def construct_from_string(cls, string):
        """
        attempt to construct this type from a string, raise a TypeError
        if its not possible
        """
        if isinstance(string, compat.string_types):
            return cls(string)
        msg = "a string needs to be passed, got type {typ}"
        raise TypeError(msg.format(typ=type(string)))
