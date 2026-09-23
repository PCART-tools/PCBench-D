    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
            self.texname == other.texname and self.size == other.size
