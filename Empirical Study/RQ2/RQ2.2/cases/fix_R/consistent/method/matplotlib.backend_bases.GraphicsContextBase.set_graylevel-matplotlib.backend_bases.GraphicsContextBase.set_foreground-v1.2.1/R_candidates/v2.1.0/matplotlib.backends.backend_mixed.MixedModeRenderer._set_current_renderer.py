    def _set_current_renderer(self, renderer):
        self._renderer = renderer

        for method in self._methods:
            if hasattr(renderer, method):
                setattr(self, method, getattr(renderer, method))
        renderer.start_rasterizing = self.start_rasterizing
        renderer.stop_rasterizing = self.stop_rasterizing
