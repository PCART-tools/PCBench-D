    def contains(self, event):
        inside, info = self._default_contains(event)
        if inside is not None:
            return inside, info
        contains, tinfo = Text.contains(self, event)
        if self.arrow_patch is not None:
            in_patch, _ = self.arrow_patch.contains(event)
            contains = contains or in_patch
        return contains, tinfo
