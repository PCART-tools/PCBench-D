    def set(self, **kwargs):
        self._construct.update(kwargs)

        self._update_rrule(**self._construct)
