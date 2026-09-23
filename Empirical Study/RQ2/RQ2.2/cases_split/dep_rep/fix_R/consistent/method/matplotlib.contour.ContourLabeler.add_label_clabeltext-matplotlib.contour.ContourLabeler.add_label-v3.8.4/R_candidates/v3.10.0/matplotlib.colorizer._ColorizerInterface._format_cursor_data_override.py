    def _format_cursor_data_override(self, data):
        # This function overwrites Artist.format_cursor_data(). We cannot
        # implement cm.ScalarMappable.format_cursor_data() directly, because
        # most cm.ScalarMappable subclasses inherit from Artist first and from
        # cm.ScalarMappable second, so Artist.format_cursor_data would always
        # have precedence over cm.ScalarMappable.format_cursor_data.

        # Note if cm.ScalarMappable is depreciated, this functionality should be
        # implemented as format_cursor_data() on ColorizingArtist.
        n = self.cmap.N
        if np.ma.getmask(data):
            return "[]"
        normed = self.norm(data)
        if np.isfinite(normed):
            if isinstance(self.norm, colors.BoundaryNorm):
                # not an invertible normalization mapping
                cur_idx = np.argmin(np.abs(self.norm.boundaries - data))
                neigh_idx = max(0, cur_idx - 1)
                # use max diff to prevent delta == 0
                delta = np.diff(
                    self.norm.boundaries[neigh_idx:cur_idx + 2]
                ).max()
            elif self.norm.vmin == self.norm.vmax:
                # singular norms, use delta of 10% of only value
                delta = np.abs(self.norm.vmin * .1)
            else:
                # Midpoints of neighboring color intervals.
                neighbors = self.norm.inverse(
                    (int(normed * n) + np.array([0, 1])) / n)
                delta = abs(neighbors - data).max()
            g_sig_digits = cbook._g_sig_digits(data, delta)
        else:
            g_sig_digits = 3  # Consistent with default below.
        return f"[{data:-#.{g_sig_digits}g}]"
