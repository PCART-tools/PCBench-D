    def __iter__(self):
        for i in range(len(self)):
            yield self._get_val_at(i)
