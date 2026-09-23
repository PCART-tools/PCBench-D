    @_api.delete_parameter("3.6", "cleared", alternative="renderer.clear()")
    def get_renderer(self, cleared=False):
        w, h = self.figure.bbox.size
        key = w, h, self.figure.dpi
        reuse_renderer = (self._lastKey == key)
        if not reuse_renderer:
            self.renderer = RendererAgg(w, h, self.figure.dpi)
            self._lastKey = key
        elif cleared:
            self.renderer.clear()
        return self.renderer
