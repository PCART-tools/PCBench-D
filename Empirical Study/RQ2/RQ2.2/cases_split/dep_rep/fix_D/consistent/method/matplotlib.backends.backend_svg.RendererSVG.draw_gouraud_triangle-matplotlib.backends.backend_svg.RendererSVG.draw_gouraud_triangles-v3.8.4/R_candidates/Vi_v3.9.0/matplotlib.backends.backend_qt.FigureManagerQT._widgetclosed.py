    def _widgetclosed(self):
        CloseEvent("close_event", self.canvas)._process()
        if self.window._destroying:
            return
        self.window._destroying = True
        try:
            Gcf.destroy(self)
        except AttributeError:
            pass
