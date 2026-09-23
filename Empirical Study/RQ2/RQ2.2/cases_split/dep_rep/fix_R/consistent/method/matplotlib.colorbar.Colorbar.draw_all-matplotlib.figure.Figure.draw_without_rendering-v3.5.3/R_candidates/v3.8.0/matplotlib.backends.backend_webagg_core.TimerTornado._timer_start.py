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
