class BlockingMouseInput(BlockingInput):
    """
    Callable for retrieving mouse clicks in a blocking way.

    This class will also retrieve keypresses and map them to mouse clicks:
    delete and backspace are a right click, enter is like a middle click,
    and all others are like a left click.
    """

    button_add = MouseButton.LEFT
    button_pop = MouseButton.RIGHT
    button_stop = MouseButton.MIDDLE

    def __init__(self, fig,
                 mouse_add=MouseButton.LEFT,
                 mouse_pop=MouseButton.RIGHT,
                 mouse_stop=MouseButton.MIDDLE):
        super().__init__(fig=fig,
                         eventslist=('button_press_event', 'key_press_event'))
        self.button_add = mouse_add
        self.button_pop = mouse_pop
        self.button_stop = mouse_stop

    def post_event(self):
        """Process an event."""
        if len(self.events) == 0:
            _log.warning("No events yet")
        elif self.events[-1].name == 'key_press_event':
            self.key_event()
        else:
            self.mouse_event()

    def mouse_event(self):
        """Process a mouse click event."""
        event = self.events[-1]
        button = event.button
        if button == self.button_pop:
            self.mouse_event_pop(event)
        elif button == self.button_stop:
            self.mouse_event_stop(event)
        elif button == self.button_add:
            self.mouse_event_add(event)

    def key_event(self):
        """
        Process a key press event, mapping keys to appropriate mouse clicks.
        """
        event = self.events[-1]
        if event.key is None:
            # At least in OSX gtk backend some keys return None.
            return
        if event.key in ['backspace', 'delete']:
            self.mouse_event_pop(event)
        elif event.key in ['escape', 'enter']:
            self.mouse_event_stop(event)
        else:
            self.mouse_event_add(event)

    def mouse_event_add(self, event):
        """
        Process an button-1 event (add a click if inside axes).

        Parameters
        ----------
        event : `~.backend_bases.MouseEvent`
        """
        if event.inaxes:
            self.add_click(event)
        else:  # If not a valid click, remove from event list.
            BlockingInput.pop(self)

    def mouse_event_stop(self, event):
        """
        Process an button-2 event (end blocking input).

        Parameters
        ----------
        event : `~.backend_bases.MouseEvent`
        """
        # Remove last event just for cleanliness.
        BlockingInput.pop(self)
        # This will exit even if not in infinite mode.  This is consistent with
        # MATLAB and sometimes quite useful, but will require the user to test
        # how many points were actually returned before using data.
        self.fig.canvas.stop_event_loop()

    def mouse_event_pop(self, event):
        """
        Process an button-3 event (remove the last click).

        Parameters
        ----------
        event : `~.backend_bases.MouseEvent`
        """
        # Remove this last event.
        BlockingInput.pop(self)
        # Now remove any existing clicks if possible.
        if self.events:
            self.pop(event)

    def add_click(self, event):
        """
        Add the coordinates of an event to the list of clicks.

        Parameters
        ----------
        event : `~.backend_bases.MouseEvent`
        """
        self.clicks.append((event.xdata, event.ydata))
        _log.info("input %i: %f, %f",
                  len(self.clicks), event.xdata, event.ydata)
        # If desired, plot up click.
        if self.show_clicks:
            line = mlines.Line2D([event.xdata], [event.ydata],
                                 marker='+', color='r')
            event.inaxes.add_line(line)
            self.marks.append(line)
            self.fig.canvas.draw()

    def pop_click(self, event, index=-1):
        """
        Remove a click (by default, the last) from the list of clicks.

        Parameters
        ----------
        event : `~.backend_bases.MouseEvent`
        """
        self.clicks.pop(index)
        if self.show_clicks:
            self.marks.pop(index).remove()
            self.fig.canvas.draw()

    def pop(self, event, index=-1):
        """
        Remove a click and the associated event from the list of clicks.

        Defaults to the last click.
        """
        self.pop_click(event, index)
        super().pop(index)

    def cleanup(self, event=None):
        """
        Parameters
        ----------
        event : `~.backend_bases.MouseEvent`, optional
            Not used
        """
        # Clean the figure.
        if self.show_clicks:
            for mark in self.marks:
                mark.remove()
            self.marks = []
            self.fig.canvas.draw()
        # Call base class to remove callbacks.
        super().cleanup()

    def __call__(self, n=1, timeout=30, show_clicks=True):
        """
        Blocking call to retrieve *n* coordinate pairs through mouse clicks.
        """
        self.show_clicks = show_clicks
        self.clicks = []
        self.marks = []
        super().__call__(n=n, timeout=timeout)
        return self.clicks
