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
