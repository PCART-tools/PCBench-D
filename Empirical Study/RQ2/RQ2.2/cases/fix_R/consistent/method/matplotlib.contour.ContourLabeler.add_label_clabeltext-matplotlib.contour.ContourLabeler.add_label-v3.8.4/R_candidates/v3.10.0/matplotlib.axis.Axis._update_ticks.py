    def _update_ticks(self):
        """
        Update ticks (position and labels) using the current data interval of
        the axes.  Return the list of ticks that will be drawn.
        """
        major_locs = self.get_majorticklocs()
        major_labels = self.major.formatter.format_ticks(major_locs)
        major_ticks = self.get_major_ticks(len(major_locs))
        for tick, loc, label in zip(major_ticks, major_locs, major_labels):
            tick.update_position(loc)
            tick.label1.set_text(label)
            tick.label2.set_text(label)
        minor_locs = self.get_minorticklocs()
        minor_labels = self.minor.formatter.format_ticks(minor_locs)
        minor_ticks = self.get_minor_ticks(len(minor_locs))
        for tick, loc, label in zip(minor_ticks, minor_locs, minor_labels):
            tick.update_position(loc)
            tick.label1.set_text(label)
            tick.label2.set_text(label)
        ticks = [*major_ticks, *minor_ticks]

        view_low, view_high = self.get_view_interval()
        if view_low > view_high:
            view_low, view_high = view_high, view_low

        if (hasattr(self, "axes") and self.axes.name == '3d'
                and mpl.rcParams['axes3d.automargin']):
            # In mpl3.8, the margin was 1/48. Due to the change in automargin
            # behavior in mpl3.9, we need to adjust this to compensate for a
            # zoom factor of 2/48, giving us a 23/24 modifier. So the new
            # margin is 0.019965277777777776 = 1/48*23/24.
            margin = 0.019965277777777776
            delta = view_high - view_low
            view_high = view_high - delta * margin
            view_low = view_low + delta * margin

        interval_t = self.get_transform().transform([view_low, view_high])

        ticks_to_draw = []
        for tick in ticks:
            try:
                loc_t = self.get_transform().transform(tick.get_loc())
            except AssertionError:
                # transforms.transform doesn't allow masked values but
                # some scales might make them, so we need this try/except.
                pass
            else:
                if mtransforms._interval_contains_close(interval_t, loc_t):
                    ticks_to_draw.append(tick)

        return ticks_to_draw
