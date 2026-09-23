    def get_renderer(self, cleared=None):
        # Mirrors super.get_renderer, but caches the old one so that we can do
        # things such as produce a diff image in get_diff_image.
        w, h = self.figure.bbox.size.astype(int)
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
            self._lastKey = key
            self._last_buff = np.copy(np.frombuffer(
                self._renderer.buffer_rgba(), dtype=np.uint32
            ).reshape((self._renderer.height, self._renderer.width)))

        elif cleared:
            self._renderer.clear()

        return self._renderer
