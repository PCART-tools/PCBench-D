    def __reduce__(self):
        return self.__class__, (list(self),)
