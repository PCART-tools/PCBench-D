class BlockingKeyMouseInput(BlockingInput):
    """
    Callable for retrieving mouse clicks and key presses in a blocking way.
    """

    def __init__(self, fig):
        super().__init__(fig=fig,
                         eventslist=('button_press_event', 'key_press_event'))

    def post_event(self):
        """Determine if it is a key event."""
        if self.events:
            self.keyormouse = self.events[-1].name == 'key_press_event'
        else:
            _log.warning("No events yet.")

    def __call__(self, timeout=30):
        """
        Blocking call to retrieve a single mouse click or key press.

        Returns ``True`` if key press, ``False`` if mouse click, or ``None`` if
        timed out.
        """
        self.keyormouse = None
        super().__call__(n=1, timeout=timeout)

        return self.keyormouse
