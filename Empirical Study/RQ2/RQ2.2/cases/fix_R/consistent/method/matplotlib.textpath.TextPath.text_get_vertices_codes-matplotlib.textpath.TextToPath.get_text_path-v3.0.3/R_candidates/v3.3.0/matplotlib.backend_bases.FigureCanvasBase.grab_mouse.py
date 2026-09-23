    def grab_mouse(self, ax):
        """
        Set the child `~.axes.Axes` which is grabbing the mouse events.

        Usually called by the widgets themselves. It is an error to call this
        if the mouse is already grabbed by another axes.
        """
        if self.mouse_grabber not in (None, ax):
            raise RuntimeError("Another Axes already grabs mouse input")
        self.mouse_grabber = ax
