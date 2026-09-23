    def __array__(self, dtype=None):
        return com._values_from_object(self)
