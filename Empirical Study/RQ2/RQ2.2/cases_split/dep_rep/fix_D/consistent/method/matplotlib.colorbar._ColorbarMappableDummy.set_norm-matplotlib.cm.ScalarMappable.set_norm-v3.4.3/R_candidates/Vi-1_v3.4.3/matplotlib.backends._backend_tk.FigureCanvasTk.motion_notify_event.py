    def motion_notify_event(self, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height - event.y
        super().motion_notify_event(x, y, guiEvent=event)
