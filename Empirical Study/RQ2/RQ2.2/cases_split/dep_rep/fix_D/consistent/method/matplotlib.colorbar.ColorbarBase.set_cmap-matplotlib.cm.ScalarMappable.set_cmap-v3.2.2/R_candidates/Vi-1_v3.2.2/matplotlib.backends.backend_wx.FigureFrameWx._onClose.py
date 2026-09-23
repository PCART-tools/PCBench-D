    def _onClose(self, evt):
        DEBUG_MSG("onClose()", 1, self)
        self.canvas.close_event()
        self.canvas.stop_event_loop()
        Gcf.destroy(self.num)
