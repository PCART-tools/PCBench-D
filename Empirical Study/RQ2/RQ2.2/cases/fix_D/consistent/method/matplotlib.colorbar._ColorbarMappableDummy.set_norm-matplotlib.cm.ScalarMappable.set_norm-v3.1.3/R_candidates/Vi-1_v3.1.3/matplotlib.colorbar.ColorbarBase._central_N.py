    def _central_N(self):
        """Return the number of boundaries excluding end extensions."""
        nb = len(self._boundaries)
        if self.extend == 'both':
            nb -= 2
        elif self.extend in ('min', 'max'):
            nb -= 1
        return nb
