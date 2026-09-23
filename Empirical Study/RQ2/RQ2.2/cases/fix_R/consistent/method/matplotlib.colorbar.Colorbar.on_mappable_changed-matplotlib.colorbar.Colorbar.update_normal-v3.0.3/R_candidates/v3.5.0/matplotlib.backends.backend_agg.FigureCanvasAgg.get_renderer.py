    def get_renderer(self, cleared=False):
        w, h = self.figure.bbox.size
        key = w, h, self.figure.dpi
        reuse_renderer = (hasattr(self, "renderer")
                          and getattr(self, "_lastKey", None) == key)
        if not reuse_renderer:
            self.renderer = RendererAgg(w, h, self.figure.dpi)
            self._lastKey = key
        elif cleared:
            self.renderer.clear()
        return self.renderer
