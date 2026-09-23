    def __init__(self, fig, interval=200, repeat_delay=None, repeat=True,
                 event_source=None, *args, **kwargs):
        # Store the timing information
        self._interval = interval
        self._repeat_delay = repeat_delay
        self.repeat = repeat

        # If we're not given an event source, create a new timer. This permits
        # sharing timers between animation objects for syncing animations.
        if event_source is None:
            event_source = fig.canvas.new_timer()
            event_source.interval = self._interval

        Animation.__init__(self, fig, event_source=event_source,
                           *args, **kwargs)
