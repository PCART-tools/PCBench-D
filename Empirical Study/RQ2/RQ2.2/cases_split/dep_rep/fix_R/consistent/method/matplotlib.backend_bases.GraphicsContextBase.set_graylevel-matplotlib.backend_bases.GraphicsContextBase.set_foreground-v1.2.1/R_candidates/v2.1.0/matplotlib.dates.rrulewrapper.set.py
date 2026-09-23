    def set(self, **kwargs):
        self._construct.update(kwargs)
        self._rrule = rrule(**self._construct)
