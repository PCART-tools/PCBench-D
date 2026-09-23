    def get_size(self, renderer):
        sz = max([
            self._get_size(ax.get_tightbbox(renderer, call_axes_locator=False),
                           ax.bbox)
            for ax in self._ax_list])
        dpi = renderer.points_to_pixels(72)
        abs_size = sz / dpi
        rel_size = 0
        return rel_size, abs_size
