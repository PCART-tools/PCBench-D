    def _single_shot_timer(self, callback):
        """Add a single shot timer with the given callback"""
        def callback_func(callback, timer):
            callback()
            self._timers.remove(timer)
        timer = self.new_timer(interval=0)
        timer.single_shot = True
        timer.add_callback(callback_func, callback, timer)
        self._timers.add(timer)
        timer.start()
