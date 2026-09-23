    def __call__(self, renderer):
        get_func = self._get_func_map[self._direction]
        vl = [get_func(ax.get_tightbbox(renderer, call_axes_locator=False),
                       ax.bbox)
              for ax in self._ax_list]
        return max(vl)
