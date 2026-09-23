    @property
    def is_monotonic(self):
        """ alias for is_monotonic_increasing (deprecated) """
        return self._engine.is_monotonic_increasing
