    def fully_contains(self, x, y):
        # Docstring inherited.
        return self._bbox.fully_contains(*self._transform.inverted().transform((x, y)))
