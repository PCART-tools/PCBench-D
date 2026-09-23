    @property
    def _is_unique(self):
        return len(unique1d(self.asi8)) == len(self)
