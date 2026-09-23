    def contains(self, mouseevent):
        # docstring inherited.
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info
        return self.patch.contains(mouseevent)
