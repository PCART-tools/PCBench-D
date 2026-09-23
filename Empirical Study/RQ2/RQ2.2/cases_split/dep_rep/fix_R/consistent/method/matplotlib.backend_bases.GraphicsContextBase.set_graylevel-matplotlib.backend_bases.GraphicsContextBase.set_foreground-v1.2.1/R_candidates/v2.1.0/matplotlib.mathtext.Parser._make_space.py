    def _make_space(self, percentage):
        # All spaces are relative to em width
        state = self.get_state()
        key = (state.font, state.fontsize, state.dpi)
        width = self._em_width_cache.get(key)
        if width is None:
            metrics = state.font_output.get_metrics(
                state.font, rcParams['mathtext.default'], 'm', state.fontsize, state.dpi)
            width = metrics.advance
            self._em_width_cache[key] = width
        return Kern(width * percentage)
