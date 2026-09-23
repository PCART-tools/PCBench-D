    def pan(self, *args):
        """
        Toggle the pan/zoom tool.

        Pan with left button, zoom with right.
        """
        if self.mode == _Mode.PAN:
            self.mode = _Mode.NONE
            self.canvas.widgetlock.release(self)
        else:
            self.mode = _Mode.PAN
            self.canvas.widgetlock(self)
        for a in self.canvas.figure.get_axes():
            a.set_navigate_mode(self.mode)
        self.set_message(self.mode)
