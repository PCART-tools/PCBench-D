    def _onLeave(self, event):
        """Mouse has left the window."""
        event.Skip()
        FigureCanvasBase.leave_notify_event(self, guiEvent=event)
