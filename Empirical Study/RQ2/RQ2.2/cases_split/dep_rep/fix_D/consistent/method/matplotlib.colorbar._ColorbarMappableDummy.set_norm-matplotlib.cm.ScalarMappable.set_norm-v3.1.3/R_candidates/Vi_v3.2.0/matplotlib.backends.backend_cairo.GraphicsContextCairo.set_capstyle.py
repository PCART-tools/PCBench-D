    def set_capstyle(self, cs):
        self.ctx.set_line_cap(cbook._check_getitem(self._capd, capstyle=cs))
        self._capstyle = cs
