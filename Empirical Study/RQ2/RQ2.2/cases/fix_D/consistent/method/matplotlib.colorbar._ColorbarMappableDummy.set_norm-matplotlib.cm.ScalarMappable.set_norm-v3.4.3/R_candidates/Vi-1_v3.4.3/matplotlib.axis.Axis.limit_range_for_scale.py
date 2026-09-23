    def limit_range_for_scale(self, vmin, vmax):
        return self._scale.limit_range_for_scale(vmin, vmax, self.get_minpos())
