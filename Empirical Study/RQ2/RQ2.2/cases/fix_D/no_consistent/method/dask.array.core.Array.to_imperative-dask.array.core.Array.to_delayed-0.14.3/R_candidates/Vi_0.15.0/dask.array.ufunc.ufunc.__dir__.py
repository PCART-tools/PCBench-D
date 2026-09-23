    def __dir__(self):
        return list(self._forward_attrs.union(dir(type(self)), self.__dict__))
