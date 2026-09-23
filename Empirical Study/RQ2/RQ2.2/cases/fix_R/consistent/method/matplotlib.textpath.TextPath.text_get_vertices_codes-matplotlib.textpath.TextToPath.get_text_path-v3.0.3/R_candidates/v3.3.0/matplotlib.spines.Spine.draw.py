    @allow_rasterization
    def draw(self, renderer):
        self._adjust_location()
        ret = super().draw(renderer)
        self.stale = False
        return ret
