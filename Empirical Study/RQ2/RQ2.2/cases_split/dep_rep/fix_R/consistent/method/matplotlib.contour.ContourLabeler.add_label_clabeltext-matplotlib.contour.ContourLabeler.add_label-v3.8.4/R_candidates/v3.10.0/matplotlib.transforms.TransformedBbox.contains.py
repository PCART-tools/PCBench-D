    def contains(self, x, y):
        # Docstring inherited.
        return self._bbox.contains(*self._transform.inverted().transform((x, y)))
