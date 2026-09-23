    def open_group(self, s, gid=None):
        # docstring inherited
        if gid:
            self.writer.start('g', id=gid)
        else:
            self._groupd[s] = self._groupd.get(s, 0) + 1
            self.writer.start('g', id=f"{s}_{self._groupd[s]:d}")
