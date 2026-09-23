    def add_axobserver(self, func):
        """Whenever the axes state change, ``func(self)`` will be called."""
        self._axobservers.append(func)
