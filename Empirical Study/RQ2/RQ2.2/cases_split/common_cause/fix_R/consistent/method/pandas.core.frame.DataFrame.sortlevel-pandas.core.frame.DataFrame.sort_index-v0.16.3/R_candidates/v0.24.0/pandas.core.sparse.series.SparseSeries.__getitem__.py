    def __getitem__(self, key):
        # TODO: Document difference from Series.__getitem__, deprecate,
        # and remove!
        if is_integer(key) and key not in self.index:
            return self._get_val_at(key)
        else:
            return super(SparseSeries, self).__getitem__(key)
