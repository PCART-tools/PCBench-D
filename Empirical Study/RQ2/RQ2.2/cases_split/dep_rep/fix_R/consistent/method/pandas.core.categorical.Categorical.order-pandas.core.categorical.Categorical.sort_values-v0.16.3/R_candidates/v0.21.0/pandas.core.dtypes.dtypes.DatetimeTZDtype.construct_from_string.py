    @classmethod
    def construct_from_string(cls, string):
        """ attempt to construct this type from a string, raise a TypeError if
        it's not possible
        """
        try:
            return cls(unit=string)
        except ValueError:
            raise TypeError("could not construct DatetimeTZDtype")
