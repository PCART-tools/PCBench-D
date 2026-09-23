    def _make_space(self, percentage: float) -> Kern:
        # In TeX, an em (the unit usually used to measure horizontal lengths)
        # is not the width of the character 'm'; it is the same in different
        # font styles (e.g. roman or italic). Mathtext, however, uses 'm' in
        # the italic style so that horizontal spaces don't depend on the
        # current font style.
        state = self.get_state()
        key = (state.font, state.fontsize, state.dpi)
        width = self._em_width_cache.get(key)
        if width is None:
            metrics = state.fontset.get_metrics(
                'it', mpl.rcParams['mathtext.default'], 'm',
                state.fontsize, state.dpi)
            width = metrics.advance
            self._em_width_cache[key] = width
        return Kern(width * percentage)
