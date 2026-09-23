    def _onSize(self, evt):
        """
        Called when wxEventSize is generated.

        In this application we attempt to resize to fit the window, so it
        is better to take the performance hit and redraw the whole window.
        """

        DEBUG_MSG("_onSize()", 2, self)
        # Create a new, correctly sized bitmap
        self._width, self._height = self.GetClientSize()
        self.bitmap = wxc.EmptyBitmap(self._width, self._height)

        self._isDrawn = False

        if self._width <= 1 or self._height <= 1:
            return  # Empty figure

        dpival = self.figure.dpi
        winch = self._width / dpival
        hinch = self._height / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)

        # Rendering will happen on the associated paint event
        # so no need to do anything here except to make sure
        # the whole background is repainted.
        self.Refresh(eraseBackground=False)
        FigureCanvasBase.resize_event(self)
