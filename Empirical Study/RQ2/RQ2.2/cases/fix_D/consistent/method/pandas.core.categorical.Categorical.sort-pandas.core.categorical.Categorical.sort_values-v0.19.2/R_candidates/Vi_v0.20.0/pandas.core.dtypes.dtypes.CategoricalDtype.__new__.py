    def __new__(cls):

        try:
            return cls._cache[cls.name]
        except KeyError:
            c = object.__new__(cls)
            cls._cache[cls.name] = c
            return c
