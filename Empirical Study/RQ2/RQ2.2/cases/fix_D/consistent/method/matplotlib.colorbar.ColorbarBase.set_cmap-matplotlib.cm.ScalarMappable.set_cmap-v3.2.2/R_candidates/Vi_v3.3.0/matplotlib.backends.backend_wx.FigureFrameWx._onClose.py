    def _onClose(self, event):
        _log.debug("%s - onClose()", type(self))
        self.canvas.close_event()
        self.canvas.stop_event_loop()
        Gcf.destroy(self)
        if self:
            self.Destroy()
