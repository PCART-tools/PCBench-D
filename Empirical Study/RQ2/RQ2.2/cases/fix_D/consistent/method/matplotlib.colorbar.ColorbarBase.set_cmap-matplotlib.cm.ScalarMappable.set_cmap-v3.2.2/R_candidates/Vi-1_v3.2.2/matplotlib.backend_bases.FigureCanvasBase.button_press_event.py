    def button_press_event(self, x, y, button, dblclick=False, guiEvent=None):
        """
        Backend derived classes should call this function on any mouse
        button press.  (*x*, *y*) are the canvas coords ((0, 0) is lower left).
        button and key are as defined in :class:`MouseEvent`.

        This method will be call all functions connected to the
        'button_press_event' with a :class:`MouseEvent` instance.
        """
        self._button = button
        s = 'button_press_event'
        mouseevent = MouseEvent(s, self, x, y, button, self._key,
                                dblclick=dblclick, guiEvent=guiEvent)
        self.callbacks.process(s, mouseevent)
