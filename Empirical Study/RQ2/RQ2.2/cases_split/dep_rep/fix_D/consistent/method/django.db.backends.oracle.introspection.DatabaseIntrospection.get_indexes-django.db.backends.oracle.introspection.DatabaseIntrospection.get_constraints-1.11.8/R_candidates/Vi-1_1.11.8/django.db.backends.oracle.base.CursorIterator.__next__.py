    def __next__(self):
        return _rowfactory(next(self.iter), self.cursor)
