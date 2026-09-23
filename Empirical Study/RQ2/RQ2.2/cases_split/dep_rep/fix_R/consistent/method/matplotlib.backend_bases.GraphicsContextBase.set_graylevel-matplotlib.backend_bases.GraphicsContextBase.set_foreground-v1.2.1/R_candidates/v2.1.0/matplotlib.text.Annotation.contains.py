    def contains(self, event):
        contains, tinfo = Text.contains(self, event)
        if self.arrow is not None:
            in_arrow, _ = self.arrow.contains(event)
            contains = contains or in_arrow
        if self.arrow_patch is not None:
            in_patch, _ = self.arrow_patch.contains(event)
            contains = contains or in_patch

        return contains, tinfo
