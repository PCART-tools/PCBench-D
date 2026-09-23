    def add_line(self, line):
        """
        Add a `.Line2D` to the Axes; return the line.
        """
        _api.check_isinstance(mlines.Line2D, line=line)
        self._set_artist_props(line)
        if line.get_clip_path() is None:
            line.set_clip_path(self.patch)

        self._update_line_limits(line)
        if not line.get_label():
            line.set_label(f'_child{len(self._children)}')
        self._children.append(line)
        line._remove_method = self._children.remove
        self.stale = True
        return line
