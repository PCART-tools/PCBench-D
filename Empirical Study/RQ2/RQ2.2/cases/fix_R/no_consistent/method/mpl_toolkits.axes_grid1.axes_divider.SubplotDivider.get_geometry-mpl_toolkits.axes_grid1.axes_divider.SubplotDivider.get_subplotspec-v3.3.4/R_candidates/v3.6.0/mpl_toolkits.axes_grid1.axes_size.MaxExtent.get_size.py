    def get_size(self, renderer):
        rel_size = 0.
        extent_list = [
            getattr(a.get_window_extent(renderer), self._w_or_h) / a.figure.dpi
            for a in self._artist_list]
        abs_size = max(extent_list, default=0)
        return rel_size, abs_size
