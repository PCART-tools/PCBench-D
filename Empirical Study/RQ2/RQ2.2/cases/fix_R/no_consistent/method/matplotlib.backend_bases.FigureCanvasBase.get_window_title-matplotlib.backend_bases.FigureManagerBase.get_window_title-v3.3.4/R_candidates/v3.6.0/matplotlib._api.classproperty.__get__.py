    def __get__(self, instance, owner):
        return self._fget(owner)
