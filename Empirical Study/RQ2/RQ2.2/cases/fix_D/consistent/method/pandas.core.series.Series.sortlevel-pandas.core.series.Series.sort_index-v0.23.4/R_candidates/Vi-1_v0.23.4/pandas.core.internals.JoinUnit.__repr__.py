    def __repr__(self):
        return '{name}({block!r}, {indexers})'.format(
            name=self.__class__.__name__, block=self.block,
            indexers=self.indexers)
