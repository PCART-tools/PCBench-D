    @property
    def is_monotonic(self):
        """ return if the index has monotonic (only equaly or increasing) values """
        return self._engine.is_monotonic
