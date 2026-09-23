    def contains(self, event):
        inside, info = self._default_contains(event)
        if inside is not None:
            return inside, info
        return self.legendPatch.contains(event)
