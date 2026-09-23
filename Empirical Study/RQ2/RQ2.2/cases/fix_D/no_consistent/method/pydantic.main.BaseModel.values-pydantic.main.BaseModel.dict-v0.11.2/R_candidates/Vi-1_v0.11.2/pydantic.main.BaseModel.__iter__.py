    def __iter__(self):
        """
        so `dict(model)` works
        """
        for k, v in self.__values__.items():
            yield k, self._get_value(v)
