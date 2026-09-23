    def get_window_extent(self, renderer=None):
        'Return extent of the legend.'
        if renderer is None:
            renderer = self.figure._cachedRenderer
        return self._legend_box.get_window_extent(renderer=renderer)
