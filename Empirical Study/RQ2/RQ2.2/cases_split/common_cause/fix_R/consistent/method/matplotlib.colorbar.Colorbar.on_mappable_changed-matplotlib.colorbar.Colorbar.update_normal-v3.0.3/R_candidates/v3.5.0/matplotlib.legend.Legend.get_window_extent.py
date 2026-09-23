    def get_window_extent(self, renderer=None):
        # docstring inherited
        if renderer is None:
            renderer = self.figure._cachedRenderer
        return self._legend_box.get_window_extent(renderer=renderer)
