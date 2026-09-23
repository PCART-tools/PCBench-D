    def add_line(self, line):
        """
        Add a :class:`~matplotlib.lines.Line2D` to the list of plot
        lines

        Returns the line.
        """
        self._set_artist_props(line)
        if line.get_clip_path() is None:
            line.set_clip_path(self.patch)

        self._update_line_limits(line)
        if not line.get_label():
            line.set_label('_line%d' % len(self.lines))
        self.lines.append(line)
        line._remove_method = self.lines.remove
        self.stale = True
        return line
