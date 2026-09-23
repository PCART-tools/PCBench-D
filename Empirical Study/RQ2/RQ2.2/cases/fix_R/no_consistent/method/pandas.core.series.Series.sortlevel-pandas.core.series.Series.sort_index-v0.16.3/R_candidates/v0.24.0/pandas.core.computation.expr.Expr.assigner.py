    @property
    def assigner(self):
        return getattr(self._visitor, 'assigner', None)
