    def set_joinstyle(self, js):
        self.ctx.set_line_join(cbook._check_getitem(self._joind, joinstyle=js))
        self._joinstyle = js
