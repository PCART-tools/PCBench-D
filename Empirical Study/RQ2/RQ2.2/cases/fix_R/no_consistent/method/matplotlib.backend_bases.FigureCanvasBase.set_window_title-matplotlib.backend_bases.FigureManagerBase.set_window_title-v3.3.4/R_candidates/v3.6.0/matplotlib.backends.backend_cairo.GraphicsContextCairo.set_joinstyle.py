    def set_joinstyle(self, js):
        self.ctx.set_line_join(_api.check_getitem(self._joind, joinstyle=js))
        self._joinstyle = js
