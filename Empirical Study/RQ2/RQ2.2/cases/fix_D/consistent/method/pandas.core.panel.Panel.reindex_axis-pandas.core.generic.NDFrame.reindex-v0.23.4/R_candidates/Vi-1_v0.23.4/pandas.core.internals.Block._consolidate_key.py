    @property
    def _consolidate_key(self):
        return (self._can_consolidate, self.dtype.name)
