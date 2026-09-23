    def _on_close(self, event):
        _log.debug("%s - on_close()", type(self))
        CloseEvent("close_event", self.canvas)._process()
        self.canvas.stop_event_loop()
        # set FigureManagerWx.frame to None to prevent repeated attempts to
        # close this frame from FigureManagerWx.destroy()
        self.canvas.manager.frame = None
        # remove figure manager from Gcf.figs
        Gcf.destroy(self.canvas.manager)
        try:  # See issue 2941338.
            self.canvas.mpl_disconnect(self.canvas.toolbar._id_drag)
        except AttributeError:  # If there's no toolbar.
            pass
        # Carry on with close event propagation, frame & children destruction
        event.Skip()
