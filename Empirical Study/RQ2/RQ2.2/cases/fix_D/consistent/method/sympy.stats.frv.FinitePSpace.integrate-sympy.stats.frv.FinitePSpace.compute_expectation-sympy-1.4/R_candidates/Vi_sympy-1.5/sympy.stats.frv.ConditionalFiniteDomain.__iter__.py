    def __iter__(self):
        return (elem for elem in self.fulldomain if self._test(elem))
