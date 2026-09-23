    def _onClose(self, event):
        _log.debug("%s - onClose()", type(self))
        self.canvas.close_event()
        self.canvas.stop_event_loop()
        # set FigureManagerWx.frame to None to prevent repeated attempts to
        # close this frame from FigureManagerWx.destroy()
        self.figmgr.frame = None
        # remove figure manager from Gcf.figs
        Gcf.destroy(self.figmgr)
        # Carry on with close event propagation, frame & children destruction
        event.Skip()
