    def set_capstyle(self, cs):
        GraphicsContextBase.set_capstyle(self, cs)
        self.gdkGC.cap_style = self._capd[self._capstyle]
