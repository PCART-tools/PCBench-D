    @property
    def _values(self):
        # We override here, since our parent uses _data, which we don't use.
        return self.values
