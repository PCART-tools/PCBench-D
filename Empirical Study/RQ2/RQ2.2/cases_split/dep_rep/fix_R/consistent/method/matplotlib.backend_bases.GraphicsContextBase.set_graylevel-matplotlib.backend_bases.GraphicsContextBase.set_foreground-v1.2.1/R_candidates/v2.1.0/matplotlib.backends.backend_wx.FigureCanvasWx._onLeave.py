    def _onLeave(self, evt):
        """Mouse has left the window."""

        evt.Skip()
        FigureCanvasBase.leave_notify_event(self, guiEvent=evt)
