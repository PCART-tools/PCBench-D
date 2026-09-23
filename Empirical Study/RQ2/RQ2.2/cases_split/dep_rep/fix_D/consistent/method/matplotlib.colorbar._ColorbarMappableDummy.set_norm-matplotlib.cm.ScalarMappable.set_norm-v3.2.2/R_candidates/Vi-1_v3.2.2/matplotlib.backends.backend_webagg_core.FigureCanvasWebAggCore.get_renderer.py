    def get_renderer(self, cleared=None):
        # Mirrors super.get_renderer, but caches the old one
        # so that we can do things such as produce a diff image
        # in get_diff_image
        _, _, w, h = self.figure.bbox.bounds
        w, h = int(w), int(h)
        key = w, h, self.figure.dpi
        try:
            self._lastKey, self._renderer
        except AttributeError:
            need_new_renderer = True
        else:
            need_new_renderer = (self._lastKey != key)

        if need_new_renderer:
            self._renderer = backend_agg.RendererAgg(
                w, h, self.figure.dpi)
            self._last_renderer = backend_agg.RendererAgg(
                w, h, self.figure.dpi)
            self._lastKey = key

        elif cleared:
            self._renderer.clear()

        return self._renderer
