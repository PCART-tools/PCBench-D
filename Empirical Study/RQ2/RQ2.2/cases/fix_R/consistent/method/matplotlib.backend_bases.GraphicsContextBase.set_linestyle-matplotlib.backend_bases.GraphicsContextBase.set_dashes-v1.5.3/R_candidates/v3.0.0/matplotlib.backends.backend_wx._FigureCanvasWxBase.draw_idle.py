    def draw_idle(self):
        """
        Delay rendering until the GUI is idle.
        """
        DEBUG_MSG("draw_idle()", 1, self)
        self._isDrawn = False  # Force redraw
        # Triggering a paint event is all that is needed to defer drawing
        # until later. The platform will send the event when it thinks it is
        # a good time (usually as soon as there are no other events pending).
        self.Refresh(eraseBackground=False)
