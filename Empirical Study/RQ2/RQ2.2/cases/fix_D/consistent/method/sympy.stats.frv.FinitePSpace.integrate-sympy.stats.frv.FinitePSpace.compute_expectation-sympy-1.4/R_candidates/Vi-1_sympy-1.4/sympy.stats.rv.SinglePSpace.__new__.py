    def __new__(cls, s, distribution):
        if isinstance(s, string_types):
            s = Symbol(s)
        if not isinstance(s, Symbol):
            raise TypeError("s should have been string or Symbol")
        return Basic.__new__(cls, s, distribution)
