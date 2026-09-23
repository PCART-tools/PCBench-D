    def timer(self):
        if self._timeout is not None and self._timeout > 0:
            timer = TimerContext(self._loop)
            self.register(timer.timeout)
        else:
            timer = TimerNoop()
        return timer
