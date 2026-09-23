    @property
    def task(self):
        return getattr(self._req, 'task', None)
