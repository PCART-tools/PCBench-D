    def open_group(self, s, gid=None):
        """
        Open a grouping element with label *s*. If *gid* is given, use
        *gid* as the id of the group.
        """
        if gid:
            self.writer.start('g', id=gid)
        else:
            self._groupd[s] = self._groupd.get(s, 0) + 1
            self.writer.start('g', id="%s_%d" % (s, self._groupd[s]))
