class TimerTornado(backend_bases.TimerBase):
    def __init__(self, *args, **kwargs):
        self._timer = None
        super().__init__(*args, **kwargs)

    def _timer_start(self):
        import tornado

        self._timer_stop()
        if self._single:
            ioloop = tornado.ioloop.IOLoop.instance()
            self._timer = ioloop.add_timeout(
                datetime.timedelta(milliseconds=self.interval),
                self._on_timer)
        else:
            self._timer = tornado.ioloop.PeriodicCallback(
                self._on_timer,
                max(self.interval, 1e-6))
            self._timer.start()

    def _timer_stop(self):
        import tornado

        if self._timer is None:
            return
        elif self._single:
            ioloop = tornado.ioloop.IOLoop.instance()
            ioloop.remove_timeout(self._timer)
        else:
            self._timer.stop()
        self._timer = None

    def _timer_set_interval(self):
        # Only stop and restart it if the timer has already been started
        if self._timer is not None:
            self._timer_stop()
            self._timer_start()
