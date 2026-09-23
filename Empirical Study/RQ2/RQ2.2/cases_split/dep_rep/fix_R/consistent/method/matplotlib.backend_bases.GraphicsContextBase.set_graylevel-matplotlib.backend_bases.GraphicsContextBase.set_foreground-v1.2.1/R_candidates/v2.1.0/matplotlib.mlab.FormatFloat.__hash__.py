    def __hash__(self):
        return hash((self.__class__, self.precision, self.scale))
