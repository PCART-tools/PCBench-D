    def set_capstyle(self, cs):
        if cs in ('butt', 'round', 'projecting'):
            self._capstyle = cs
            self.ctx.set_line_cap(self._capd[cs])
        else:
            raise ValueError('Unrecognized cap style.  Found %s' % cs)
