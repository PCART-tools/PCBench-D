    def get_renderer(self, cleared=False):
        l, b, w, h = self.figure.bbox.bounds
        key = w, h, self.figure.dpi
        try:
            self._lastKey, self._renderer
        except AttributeError:
            need_new_renderer = True
        else:
            need_new_renderer = (self._lastKey != key)

        if need_new_renderer:
            self._renderer = RendererAgg(w, h, self.figure.dpi)
            self._lastKey = key
        elif cleared:
            self._renderer.clear()

        return self._renderer
