    def set_joinstyle(self, js):
        GraphicsContextBase.set_joinstyle(self, js)
        self.gdkGC.join_style = self._joind[self._joinstyle]
