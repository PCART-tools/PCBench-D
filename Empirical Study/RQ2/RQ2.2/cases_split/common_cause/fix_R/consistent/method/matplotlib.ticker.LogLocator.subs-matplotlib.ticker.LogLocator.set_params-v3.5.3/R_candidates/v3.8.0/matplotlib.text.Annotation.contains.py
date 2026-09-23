    @_api.rename_parameter("3.8", "event", "mouseevent")
    def contains(self, mouseevent):
        if self._different_canvas(mouseevent):
            return False, {}
        contains, tinfo = Text.contains(self, mouseevent)
        if self.arrow_patch is not None:
            in_patch, _ = self.arrow_patch.contains(mouseevent)
            contains = contains or in_patch
        return contains, tinfo
