    def _different_canvas(self, event):
        """
        Check whether an *event* occurred on a canvas other that this artist's canvas.

        If this method returns True, the event definitely occurred on a different
        canvas; if it returns False, either it occurred on the same canvas, or we may
        not have enough information to know.

        Subclasses should start their definition of `contains` as follows::

            if self._different_canvas(mouseevent):
                return False, {}
            # subclass-specific implementation follows
        """
        return (getattr(event, "canvas", None) is not None and self.figure is not None
                and event.canvas is not self.figure.canvas)
